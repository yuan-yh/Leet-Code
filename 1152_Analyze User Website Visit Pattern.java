class Solution {
    public List<String> mostVisitedPattern(String[] username, int[] timestamp, String[] website) {
        // 1. sort user visit based on timestamps
        List<String[]> sorted = new ArrayList<>();
        for (int i = 0; i < timestamp.length; i++) {
            sorted.add(new String[]{username[i], String.valueOf(timestamp[i]), website[i]});
        }
        sorted.sort((a, b) -> Long.compare(Long.parseLong(a[1]), Long.parseLong(b[1])));

        // 2. record visit history for each user based on timestamp
        Map<String, List<String>> visit = new HashMap<>();
        for (int i = 0; i < sorted.size(); i++) {
            String[] tmp = sorted.get(i);
            visit.putIfAbsent(tmp[0], new ArrayList<>());
            visit.get(tmp[0]).add(tmp[2]);
        }

        // 3. extract pattern for each user & count frequency
        Map<List<String>, Integer> patternCount = new HashMap<>();
        for (Map.Entry<String, List<String>> entry : visit.entrySet()) {
            Set<List<String>> patternPerUser = new HashSet<>();
            List<String> webHisPerUser = entry.getValue();

            for (int i = 0; i < webHisPerUser.size() - 2; i++) {
                for (int j = i+1; j < webHisPerUser.size() - 1; j++) {
                    for (int k = j+1; k < webHisPerUser.size(); k++) {
                        // record pattern w/n repeat in one user's web history
                        List<String> tmp = Arrays.asList(webHisPerUser.get(i), webHisPerUser.get(j), webHisPerUser.get(k));
                        patternPerUser.add(tmp);
                    }
                }
            }
            // update the pattern frequency
            for (List<String> pattern : patternPerUser) {
                patternCount.put(pattern, patternCount.getOrDefault(pattern, 0) + 1);
            }
        }
        // 4. find the most frequent pattern
        List<String> res = new ArrayList<>();
        int maxCount = -1;

        for (Map.Entry<List<String>, Integer> entry : patternCount.entrySet()) {
            if (entry.getValue() > maxCount) {
                res = entry.getKey();
                maxCount = entry.getValue();
            }
            else if (entry.getValue() == maxCount) {
                // find the lexicographically smaller one
                List<String> tmp = entry.getKey();
                for (int i = 0; i < 3; i++) {
                    if (res.get(i).compareTo(tmp.get(i)) < 0) break;
                    else if (res.get(i).compareTo(tmp.get(i)) == 0) continue;
                    else {
                        res = tmp;
                        break;
                    }
                }
            }
        }

        return res;
    }
}
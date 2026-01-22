class Solution:
    def intToRoman(self, num: int) -> str:
        # Given range: 1 <= num <= 3999
        prefix = (
            ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"),     # 个位
            ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"),     # 十位
            ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"),     # 百位
            ("", "M", "MM", "MMM")      # 千位
        )

        return prefix[3][num//1000] + prefix[2][(num%1000)//100] + prefix[1][(num%100) // 10] + prefix[0][(num%10)]
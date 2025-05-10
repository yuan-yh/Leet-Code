public class MyClass {
    static int count = 0;   // 静态变量

    // 静态方法
    public static void incrementCount() {count++;}

    public static void printStaticVar() {
        System.out.println("Static Var: " + count);
    }
}

// 使用示例
MyClass.incrementCount();   // 调用静态方法
MyClass.printStaticVar();   // 输出 Static Var: 1
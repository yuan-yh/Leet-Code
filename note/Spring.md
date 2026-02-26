# Backend - Spring
## Spring
### 单例模式（Singleton Pattern）
一个类在整个应用中只创建一个实例，所有地方共用这同一个对象。

**为什么需要单例？**
- 如果每次处理请求都创建一个新的数据库连接对象，一秒钟几千个请求就意味着几千个连接对象，内存很快就炸了。而像数据库连接、配置管理这类东西，本身就不需要多个实例，共用一个就够了。

**Spring 中的单例**
Spring 默认就是单例的。

- 不是说所有 new 出来的对象都是单例。Spring 只管它容器里的对象，也就是那些你用 @Service、@Controller、@Repository、@Component 标注的类。Spring 容器里托管的 Bean 默认是单例的，普通 Java 对象该怎么 new 还是怎么 new。

- For `@Autowired`, Spring 启动时会创建一个 OrderService 实例，放进它的容器（IoC Container）里。之后不管多少地方注入这个 Service，拿到的都是同一个对象。

### Bean
Bean 就是 Spring 容器帮你创建和管理的对象。只要一个类被特定注解标注，Spring 启动时就会自动创建它的实例，放进容器里，这个实例就叫 Bean。

```这些注解会让一个类成为 Bean
@Component（最通用的）
@Service（本质就是 @Component，语义上表示业务逻辑层）
@Repository（本质也是 @Component，语义上表示数据访问层）
@Controller / @RestController（本质也是 @Component，语义上表示控制器）
```

- Bean（Spring 管理）：那些"工具类"——Service、Repository、Controller，整个应用只需要一个，大家共用

- 非 Bean（你自己管理）：那些"数据类"——Entity、DTO、Request/Response 对象，每次请求都可能创建新的

- 之後要用的時候, `@Autowired`：从 Spring 容器里拿一个已经存在的 Bean 赋给变量

- 单例 Bean 不要用实例变量保存请求数据，要用局部变量。


## MVC
经典架构模式，把应用分成三层：

1. Model（模型）：Server-Side
- 业务逻辑 + 数据访问
    1.1 Entity / POJO：映射数据库表 (like DB schema)，纯粹描述数据结构
    - Why need Entity? ORM（Object-Relational Mapping，对象关系映射）
    - 核心原因：Java 是面向对象的语言，而数据库是关系型的表结构。这两者之间需要一个"翻译"，Entity 就是这个翻译层 。
    - @Entity 不是 Bean，Spring 不管理它的实例

    1.2 Repository / DAO：负责跟数据库打交道（增删改查）
    - Repository 把 SQL 操作封装成了 Java 方法调用，你不用手写 SQL。

    1.3 Service：Business Logic，调用 Repository 来操作数据库

> 分层架构的意义——解耦: 如果以后业务逻辑变了，你只改 Service；如果换数据库，你只改 Repository；Controller 基本不用动。

2. View（视图）：Client-Side
- 现在前后端分离的项目中，View 通常就是前端（React、Vue 等），后端只返回 JSON 数据。

3. Controller（控制器）：Router
- 负责接收用户请求，调用 Model 处理业务，然后把结果返回给 View。它是 Model 和 View 之间的桥梁。

用一个实际例子理解：
假设用户访问 /users/1 想查看某个用户的信息：

Controller 接收到这个请求
Controller 调用 Model 层（Service → Repository）去数据库查出用户数据
Controller 把数据返回给 View 展示

### WorkFlow*
```完整的生命周期
Spring 启动
    ↓
扫描所有类，发现 @Service、@Repository、@Controller 等注解
    ↓
为每个标注的类创建一个实例（Bean），放进容器
    ↓
处理 @Autowired，发现 OrderController 需要 OrderService
    ↓
从容器里找到 OrderService 的 Bean，赋值给 OrderController 的 orderService 字段
    ↓
启动完成，等待请求
```

### 依赖注入（Dependency Injection, DI）
把"我需要用到的东西"从外部塞给我 (从容器里找到Bean -> 赋值)，而不是我自己去new。

### 控制反转（Inversion of Control, IoC）
From Dev-Control to Frame-Control

1. "控制"指的是谁来决定创建对象、管理对象的生命周期。

- 传统方式下，控制权在你手上：你决定什么时候创建，创建什么
```java
OrderService orderService = new OrderService();
OrderRepository orderRepository = new OrderRepository();
// 你还得知道 OrderService 需要 OrderRepository，手动组装
orderService.setOrderRepository(orderRepository);
```

- Spring: 控制权交给了 Spring 容器：你什么都不管，只声明需要什么
```java
@Autowired
private OrderService orderService;
// Spring 负责创建、组装、管理
```

2. "反转"就是指这个控制权从你（开发者）转移到了框架（Spring）。以前你主动去创建和组装对象，现在你被动接收 Spring 

3. IoC 是思想，DI 是 IoC 的具体实现方式。


## Spring Boot
> 传统的 Spring 项目需要大量的 XML 配置或 Java 配置类，Spring Boot 把大部分配置都默认处理好了，让你能专注于业务代码。

### Popular Questions
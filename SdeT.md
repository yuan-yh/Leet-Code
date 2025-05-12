## Job Description
**CI持续集成**
（频繁的代码合并和单元测试，快速反馈集成结果）
在开发过程中，开发人员需要不断地将代码提交到仓库，为了保证合并后的代码可用性，每次提交后需要进行编译，测试，和部署。为了提高这一环节的效率，我们使用自动化集成：每次代码提交后，将自动触发编译、单元测试和部署。一旦编译失败，我们将自动通知开发人员来修复代码。理论上我们鼓励频繁的上传更新的代码，这样可以在代码错误影响较小时及时更正，避免问题在代码中逐渐累积。

**CD** (分为两个层次)
（交付前进一步确定提交的代码在整体软件中的可用性与稳定性，确保应用的质量达到交付标准，随时可以发布到生产环境）
**持续交付（Continuous Delivery）**
在通过持续集成后，将代码部署到类生产环境（Pre-Production Environment, like staging / UAT），但不自动发布到生产环境（Production Environment - 用户实际使用的正式环境）。需要由开发或运维人员手动触发把应用交付到生产环境。这种手动触发可以让团队在发布前做最后的检查，确保产品符合预期，从而进一步降低应用在生产环境中可能出现的风险。
**持续部署（Continuous Deployment）**
在通过持续集成后，自动触发发布到生产环境，无需人工干预。全流程自动化，适合测试覆盖率极高的团队。风险在于需要完善的自动化测试和监控兜底。
（总的来说，从集成到生产环境的全自动化极大缩短了软件发布周期，提高交付效率）
**实现**
- Jenkins：支持豐富的插件
- GitLab：一個功能豐富的代碼存儲平臺
- Argo CD：基於k8s的持續交付系統，只能在k8s上使用

## Self-Introduction
Hi，我叫{NAME}，是cs专业的硕士生。我作为software developer有6个月的实习经验，主要做的是全栈开发这一块，也有实施过单元测试、集成测试、和e2e端到端测试。
我对测试岗位很有兴趣，因为我认为测试是一个兼具了开发和用户视角的关键角色，可以更好地完善产品，而且我自己也很喜欢找bug。
My name is Yuan, a master CS student. I have 6-month internship experience as a software developer and most work in the field of full-stack web development with hands-on experience in unit test, integration test, and E2E test.

## Internship Deep-Dive
### General Workflow
1. Planning: Jira Board将问题和开发任务指派给具体负责人
2. UI & Interface Design: MockFlow & API documentation
3. Coding: GitHub
4. Building: Jenkins自动化持续集成、测试、部署
5. Testing: Playwright自动对应用的功能测试
6. Releasing: Nexus Repo集中管理软件包
7. Deploying: Kubernetes承载应用的基础设施，所有应用程序都在k8s集群中运行
8. Maintaining: Grafana & Prometheus监控基础设施，包括k8s、服务器、应用程序等

一般是后端根据需求先构建数据模型，然后出接口文档-前端同时画页面，然后后端实现接口逻辑同时前端mock接口，填充页面，下来联调，转测，上线

### Tech Stack
#### Architecture Overview
The app follows a layered architecture (分层架构): *Electron bridges the frontend and backend, allowing Node.js access.*
- **Frontend (Renderer Process)**: 
	- Vue handles the UI; Pinia for state management; TypeScript adds type safety
	- Vue处理UI， Pinia进行状态管理，TypeScript增加类型安全
- **Backend (Main Process)**: 
	- Electron’s Node.js runtime manages PostgreSQL interactions, file I/O, and other OS-level tasks.
	- Electron的Node.js管理PostgreSQL交互，文件I/O和其他操作系统级任务
- **Database**: PostgreSQL stores and serves structured data (via Knex).
- Electron IPC bridges the frontend and backend.

#### 从浏览器用户操作到网页显示，期间App层面发生了什么
User Interaction Workflow - Loading Users
1. **User Interaction (用户交互)**: 
	1. A button click in a Vue component triggers `userStore.fetchUsers()`.
	2. 点击Vue组件中的按钮会触发‘ userStore.fetchUsers() ’
2. **Pinia Action**:
	1. The Pinia store invokes `window.electron.ipcRenderer.invoke('fetch-users')`.
	2. Pinia商店调用
3. **IPC to Main Process**:
	1. The main process’s `ipcMain` handler receives the `fetch-users` event.
	2. 主进程的‘ ipcMain ’处理器接收‘ fetch-users ’事件
4. **Database Query**:
	1. The main process runs `queryUsers()`, which borrows a connection from the pool and executes a PostgreSQL `SELECT * FROM users`, then returns the connection to the pool.
	2. 主进程运行‘ queryUsers() ’，从池中借用连接，执行PostgreSQL ‘ SELECT * FROM users ’，将连接返回到池中
5. **Response**:
	1. Data is sent back to the renderer process via IPC.
	2. 数据通过IPC发送回渲染进程
6. **UI Update**:
	1. Pinia updates its `users` state, and Vue reactively re-renders the component.
	2. Pinia更新它的“用户”状态，Vue重新渲染组件

#### Electron
1. How does Electron work?
- Electron structure: main + renderer + (prerender / preload)
- The main process runs Node.js and handles database operations, while the renderer process manages the UI.
- They communicate via IPC.
- **When the UI needs data, it sends a message from the renderer to the main process, which queries the database and sends back the result.**

Here’s a simplified diagram:
```
Vue Components → Pinia Store → Electron IPC → Main Process (Node.js) → PostgreSQL
```

2. How does **IPC** (Inter-Process Communication) work?
- In Electron, the *main* process (backend) and the *renderer* process (frontend) run separately and can’t talk directly, so they use **IPC** to send messages back and forth.
- *Main*: send / receive notes (messages) using `ipcMain`.
- *Renderer*: send / receive notes using `ipcRenderer`.
- ' ipcRenderer ' →用于在Renderer中发送请求到Main, ' ipcMain ' →在Main中监听事件，执行逻辑（例如，查询PostgreSQL），并返回结果。
	Why we need IPC?
- 安全：如果Renderer有完整的Node.js访问权限，黑客可能会滥用它（例如，删除文件）
- 分离：保持UI代码（Renderer）和后端逻辑（Main）干净和独立。

3. Why include the **preload** process?
Background Information: 
- 提前公开特定的API地给渲染器进程, 限制在渲染器中直接访问Node.js来防止安全风险
- While the *main* process as the backend and the *renderer* as the frontend, the *preload* process is a bridge between the *main* and *renderer* processes.
- It runs before the *renderer* process loads, which is used to **expose specific APIs** safely to the *renderer* process. 
- The goal is to prevent security risks by limiting direct Node.js access in the renderer.

#### Frontend
##### Vue
- Render the UI (e.g., display user data) & trigger actions (e.g., a button click to fetch data).
- 呈现UI（例如，显示用户数据的表）, 触发动作（例如，点击按钮获取数据）。
###### Lifecycle Hook
Source: https://cn.vuejs.org/guide/essentials/lifecycle
**创建阶段（Creation）- 初始化数据，调用api**
- `setup()`: (组合式Composition API only)
- 在组件创建前运行。用于定义响应数据、计算属性、方法和其他钩子。

- `beforeCreate`: (选项式Options API only)
- 在组件初始化之后，但在响应性数据和事件设置之前运行；主要用于高级插件集成。

- `created`: (选项式Options API only)
- 在组件初始化、响应数据设置之后运行，但在模板呈现之前运行。
- 获取初始数据，设置非响应性属性。

**挂载阶段(Mounting - DOM Insertion) - 访问DOM元素，初始化第三方库**
- `onBeforeMount`: (组合式Composition API only)
- 在组件渲染到DOM之前运行。

- `mounted`(选项式Options API) / `onMounted` (组合式Composition API)
- 在组件被渲染并插入DOM后运行。
- 访问DOM，初始化库（例如，图表，地图），或获取需要DOM元素的数据。

**更新阶段 (Update - Reactivity Changes) - 对DOM变化作出反应**
- `onBeforeUpdate` (组合式Composition API)
- 在数据改变时，但在DOM被重新渲染之前运行。

- `updated` (选项式Options API) / `onUpdated` (组合式Composition API)
- 在Vue更新DOM后执行操作（小心使用以避免无限循环）。

**卸载阶段 (Unmounting - Component Destruction) - 清理**
- `onBeforeUnmount` (组合式Composition API)
- 在组件从DOM中移除之前运行（例如，移除事件监听器，取消计时器）。

- `unmounted` (选项式Options API) / `onUnmounted` (组合式Composition API)
- 在组件被销毁并从DOM中移除后运行 （例如，处理外部库）。

Extra: Error Handling
- `onErrorCaptured` (组合式Composition API): 从子组件捕获错误

###### Pinia
- Hold reactive application state (e.g., users: User[]). & expose actions to fetch/update data. 
- 保持响应式应用状态（例如，users: User[]）, 暴露操作来获取/更新数据。
- State management is a crucial for helping manage shared data across components. (帮助管理跨组件的共享数据)

##### TypeScript: 定义接口类型
- Type Safety
- Define interfaces for data shapes (e.g., `User` interface for PostgreSQL records):
```typescript
// types/user.ts
export interface User {
id: number;
name: string;
email: string;
}
```
- Enforce types in Pinia stores, IPC calls, and database queries.
#### Backend
- Database Layer: use **Knex.js** (or TypeORM) to interact with PostgreSQL.
- Connection Pooling (连接池):
	- Reuse database connections to avoid overhead (configured via `pg-pool` in Knex).	
Background Information
- Every database query (e.g., `SELECT`, `INSERT`) requires a connection, while opening/closing connections for every query is slow and resource-heavy. Therefore, a connection pool maintains a set of pre-established connections that can be reused. 
- 每个数据库查询（例如，SELECT，INSERT）都需要一个连接，而每个查询打开/关闭连接是缓慢且占用资源的。因此，连接池维护一组可以重用的预先建立的连接。
- 性能快（重用连接）, 优化资源使用（受‘ max ’限制）, 并发: 池忙时排队查询
- Workflow: 
App Starts -> Knex initializes the pool (e.g., `min: 2` connections, `max: 10` connections).
Query Executes -> App borrows a connection from the pool -> Runs the SQL query -> Returns the connection to the pool (instead of closing it).
	If all connections are busy, new queries wait (up to `acquireTimeoutMillis`).
	If a connection is idle too long (`idleTimeoutMillis`), it’s closed.
App Exits -> Close the Pool

#### Testing
##### Frontend Test
**Vue / Pinia Test**
Source: https://cn.vuejs.org/guide/scaling-up/testing

**Unit Test** on 组合式函数 (Composables, like useMouse) & 组件
Tool: Vitest @vue/test-utils (based on Vite - fast & easy to integrate in Vite project), Jest
Method: 
- Whitebox 白盒
知晓一个组件的实现细节和依赖关系。它们更专注于将组件进行更 **独立** 的测试。这些测试通常会涉及到模拟一些组件的部分子组件，以及设置插件的状态和依赖性（例如 Pinia）。
- Blackbox 黑盒
黑盒测试不知晓一个组件的实现细节。这些测试尽可能少地模拟，以测试组件在整个系统中的集成情况。它们通常会渲染所有子组件，因而会被认为更像一种“集成测试”。
	
**Component Test** on Vue components for rendering correctness
Tool: Vitest @vue/test-utils

###### IPC Call
Use `jest.mock` to mock Electron IPC calls, isolating frontend logic. 
```
// __mocks__/electron.ts  
export const ipcRenderer = { invoke: jest.fn(() => Promise.resolve(mockInvoices)) };  
```

##### Backend Test
###### Integration Test (Docker / knex / Jest)
- Tool: `Jest`, `knex` migrations/seeds, and Dockerized test databases.
- Goal: 测试Node.js REST API端点 + PostgreSQL query逻辑 + 响应时间
	- **测试从API调用到查询执行再返回的整个流程。**
	
0. **Docker创建一次性容器运行数据库→knex植入数据→Jest运行测试→测试后销毁容器**
1. Dockerized PostgreSQL：在一个隔离的一次性容器中运行数据库（PostgreSQL）进行测试。
	1. 确保测试在干净、一致的数据库状态下运行（不与开发/生产数据冲突）。
	2. **Isolation**
	3. Collaboration: 通过Docker Compose配置文件（预配置的PostgreSQL实例）共享测试环境。
2. `knex` Migrations：定义数据库Schema
	1. Define database schema (tables, columns)
3. `knex` Seeds：插入测试数据
	1. Insert test data
	2. **Reproducibility**: same database state every time.
4. Jest: 运行测试，测量 `fetchInvoiceById` 检索种子数据的速度。
	1. 验证逻辑/性能: Validates logic/performance (e.g., query speed -  after adding a database index via `knex` migrations)
5. 容器在测试后销毁。

```
# 1. Start a test PostgreSQL container 
docker run --name test_db -e POSTGRES_PASSWORD=test -p 5432:5432 -d postgres 

# 2-3. Run migrations/seeds to set up the schema + test data
npx knex migrate:latest 
npx knex seed:run 

# 4. Execute tests (Jest) 
npm test
```
Sample Jest Test: 
```
// 4. Jest Test: tests/invoiceQueries.spec.ts
test('fetchInvoiceByID returns data in <100ms', async () => {
  const start = Date.now();
  await fetchInvoiceById('123');  // Queries the Dockerized DB
  expect(Date.now() - start).toBeLessThan(100);
});
```

###### E2E Test
- Tool: `Playwright` or `Cypress`
	- Automate browser interactions（如点击按钮，填写表单）
	- 跨进程测试（UI→IPC→PostgreSQL），在不同的系统层测试整个流程。

### Deep-Dive
#### 1 - (总结)可扩展/日交易量增长
Statement: Architected and implemented a scalable full-stack billing management app using **Vue**, **TypeScript** and **Electron**, collaborating with **cross-disciplinary** teams, which supported a **25%** increase in daily transaction volume
##### STAR 总结
在这段实习中，我主導开发了一个桌面端的账单管理系统，用于管理产品与其对应的发票信息。

原先公司内部使用的是一个基于 C 开发的旧系统，随着业务扩展和数据体量的增长，這個应用在稳定性和功能可扩展性方面已经无法满足日常业务需求，比如查询效率低、发票信息冗余严重，影响了finance部門的处理效率。

所以我们的目标是构建一个更高效、可扩展的新系统，提升发票管理、产品信息录入与查询的整体性能。我作为实习生，承担了前端页面开发、后端接口设计与实现，以及数据库优化、自动化测试，從頭到尾（笑）。

- 我使用 **Vue** **和 TypeScript** 设计并实现了关键页面的组件结构，重构了发票展示与编辑模块，通过优化状态管理和组件渲染逻辑，使页面加载时间减少了 **20%**；
- 在后端，我使用 **Node.js** **与 Express** 编写和维护了多组 **RESTful API**，用于发票与产品数据的交互，并通过改进数据结构，提升数据一致性达 **30%**；
- 我还参与数据库重构，优化了 **SQL** **查询语句** 与索引策略，降低冗余数据 **35%**，提升了查询响应速度 **40%**，面对 **5** **万条以上**的产品数据依然能保持流畅；
- 最后，我搭建了基于 **Docker** **的 CI/CD** **管道**，实现了 100% 的自动化单元测试与集成测试覆盖，使部署效率提高了 **50%**。

项目成功交付后，系统每日处理账单量提升了 **25%**，用户满意度显著提升。这个项目让我学会了如何从全栈视角出发，系统性地提升产品性能与质量。我也更深刻理解了测试在实际开发流程中所起的关键作用。
##### Metrics (25% daily transaction)
进行为期一周的**A/B测试**，将50%的用户引导到原本的应用程序，50%引导到新的electron应用程序。通过跟踪交易完成量，我们发现新应用的完成率提高了30%。

##### Why tech stack (Vue + TypeScript + Electron)
- Vue: 轻量级和快速渲染, 允许与现有系统逐步集成, 清晰的状态管理
	- better performance and stability
- TypeScript: 通过强制类型检查减少事务处理中的运行时错误，有助于数据一致性
- Electron: 执行速度 + 安全 + 稳定 + UI一致性
	- Why 桌面应用desktop app:
		- 桌面应用在OS上本机运行，执行更快，Web应用取决于网速和浏览器性能。
		- 没有基于浏览器的威胁: 
			- IT团队可以执行安全策略（防火墙规则、加密），Web应用易受会话劫持。
		- 桌面应用不依赖浏览器，没有网站被关闭的风险，即使开发人员停止云服务也能工作。Web应用需要主动维护（后端服务器/API成本, e.g.浏览器更新（如Chrome弃用api）会破坏功能）, 中断服务可能导致应用程序无法使用。
		- UX: Web应用受浏览器功能限制，桌面应用遵循OS原生设计，导致更好的可用性。
		- 完整的硬件控制
- 考虑了哪些权衡: 
	- Vue组件: 实现了代码分割(code splitting)和延迟加载(lazy loading), 以减少初始加载时间和内存使用。
	- Pinia: 优化状态管理以避免不必要的重新渲染。

##### 可扩展性 Scalability
- Definition: 系统在保持性能、可维护性和可扩展性的同时增加复杂性 (features, data, etc)
- **Modular Architecture (模块化架构)**
	- 分离UI、业务逻辑和数据层，以允许独立扩展。
	- Component/Service Decoupling (组件/服务解耦)
		- 将app组织成离散的、可重用的组件（Vue）和service（TypeScript类）, 每个模块应该有一个单独的职责，并公开清晰的接口。
	- Electron Process Separation (进程分离)
		- Main Process
			- 处理本地操作系统交互（文件I/O，系统对话框）
			- 在孤立的线程中进行繁重的计算，以避免阻塞UI。
		- Renderer Process
			- 通过IPC（进程间通信）将逻辑卸载到主进程，从而保持Vue组件的轻量级。
			- 使用异步IPC来防止UI冻结
	- 结合Vue的反应性、TypeScript的严谨性和Electron的进程隔离
- **Modular Design (模块化设计)**
	- 分离产品信息服务（handles product info）和发票服务（manage invoices）。
		- Loose Coupling松散耦合
			- 模块通过定义良好的接口（如api、事件）进行交互，但不直接访问其数据库。
		- 独立开发部署: 团队可以单独开发每个模块。
		- 可伸缩性
			- 高需求服务（例如，产品查找）可以独立于发票进行扩展。
潜在的扩展性瓶颈
- 数据库写争用 (Write Contention): 在高峰时间，并发的发票更新导致表锁(table lock), 可以通过切换到行级锁定(row-level locking)和批处理(batching writes)写来解决这个问题。
##### 合作Collaboration
我们每周与产品、财务和QA团队进行一次同步，以使技术决策与业务目标保持一致。
- 例如: 财务团队优先考虑优化发票编辑流程，因此我们改进了搜索流程(基于制造商、经销商、开票方、地区), 帮助他们更容易找到要编辑的发票。

#### 2 - (前端)优化组件渲染和状态管理/减少页面加载时间
Statement: Revamped invoice dashboards using Vue.js, achieving a **20%** reduction in page load time by optimizing component rendering and state management, which enhanced user engagement by **15%**
##### 綜述
我做了几个前端方面的优化：

首先是 **组件懒加载**。原来的页面会一次性加载所有发票相关的组件，比如图表、历史记录、客户明细等等，导致首屏加载特别慢。我用 `defineAsyncComponent` 搭配 Vue Router 实现了按需加载，让这些“重组件”只有在用户点进去看的时候才加载，这样能大幅减少初始加载资源。

第二是 **渲染优化**。发票页面里的表格数据很多。我用 `computed` 和 Vue 3.3 里的 `v-memo`（或类似的记忆化逻辑）来避免不必要的重新渲染。比如说如果只是更新了客户信息，整个表格就不会重绘，这样性能能稳定很多。

然后是 **状态管理的调整**。原本我们的 Pinia store 是集中式的，很多状态绑在一起，一个变动就会触发很多组件更新。我把它们拆分成了模块化的 store，像发票、客户、统计信息都分开管理，让每个组件只订阅自己需要的数据，这样也减少了不必要的更新。

至于性能改善的数据，**页面加载时间减少了大约 20%**，我是用 Chrome DevTools 的 Performance 面板来量的，特别是看 LCP（最大内容绘制），优化前后对比，大概减少了 20.8%。

**用户参与度提升**的部分，我们主要關注页面停留时间、操作次数这些指标，后来我和mentor合作接入了 Mixpanel，数据显示优化之后参与度提高了大约 15.6%。

##### 如何优化组件渲染和状态管理 (Page Load)
- Source: Page Load: https://cn.vuejs.org/guide/best-practices/performance.html
- 组件渲染 (懒加载 / Memoization - see below)
	- 懒加载: 按需加载
	- Memoization: 应用`Computed`属性和`v-memo`避免大列表(1000+行)的冗余重新渲染
- 状态管理 (Pinia: 分割global store)
**集中状态管理(Pinia)**：使用状态管理库来避免组件级数据的分散状态。
- Pinia提供了组合式风格的 API，最重要的是，在使用 TypeScript 时提供了更完善的类型推导。
	- 类型推导是指 TypeScript 编译器能根据上下文自动推断出变量、函数参数或返回值的类型，而无需开发者显式指定类型注解。
- 将全局状态分割成多个逻辑模块（stores）
	- 更细粒度的更新：修改发票数据不会触发客户相关组件的更新
		- **减少不必要的重新渲染**：组件只订阅它们实际需要的状态
	- 更好的代码组织：相关状态和逻辑集中管理
	- 更小的打包体积：支持代码分割，**按需加载stores**

##### Lazy Loading & Dynamic Import懒加载和动态导入
- 将Vue组件和Electron模块拆分为**按需加载**的块（例如，通过‘ import() ’或Vue Router惰性加载）。
- 使用Vue Router的`defineAsyncComponent`动态导入heavy component（例如，图表、数据网格），确保只在可见时加载（例如，通过Intersection Observer API或基于路由的拆分）。
	- 路由懒加载: https://router.vuejs.org/zh/guide/advanced/lazy-loading.html
	- 当打包构建应用时，JavaScript 包会变得非常大，影响页面加载。
	- 把不同路由对应的组件分割成不同的代码块，然后当路由被访问的时候才加载对应组件，会更加高效。

##### Page Load Metrics (20%)
- Definition - 页面加载性能：首次访问时，应用展示出内容与达到可交互状态的速度。
- Chrome DevTools Profiler
	- 这通常会用 Google 所定义的一系列 Web 指标 (Web Vitals) 来进行衡量，如最大内容绘制 (Largest Contentful Paint，缩写为 LCP) 和交互至下一次绘制 (INP)。
	- Example: LCP: 4.8s (优化前, 包含发票表格渲染) -> 3.8s (优化后, ≈20%提升)
	- 关键影响因素
		- 资源加载优化：
			- 图片懒加载 → 减少主线程竞争
			- 关键CSS内联 → 加速视觉稳定
		- 渲染优化：
			- 组件静态化（如冻结非视窗表格行）
			- 避免大型渲染阻塞任务

##### User Engagement (15%)
- 选择以下**简易指标**来衡量用户参与度: 0.5*页面停留时间 + 0.5*用户操作次数
	- 优化前后的平均页面停留时间、操作次数进行对比
- (future) 集成Mixpanel分析用户行为, 跟踪关键事件（例如，“发票编辑”，“发票过滤”）。优化后每个用户的日均会话: 3.2次 → 3.7次, 提升了15.6%。
```
let startTime: number;

export default {
  mounted() {
    startTime = Date.now();
    window.addEventListener("beforeunload", this.trackTimeOnPage);
    document.addEventListener("click", this.trackClick);
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.trackTimeOnPage);
    document.removeEventListener("click", this.trackClick);
  },
  methods: {
    trackTimeOnPage() {
      const stayDuration = Date.now() - startTime;
      console.log(`用户停留时间: ${(stayDuration / 1000).toFixed(2)} 秒`);
      // 可以发送到后端：axios.post('/metrics', { stayDuration })
    },
    trackClick() {
      // 每点击一次记录
      console.log("用户点击了一次");
      // 可以累加发送：axios.post('/metrics', { event: 'click' })
    }
  }
};

```

#### 3 - (后端)REST API/优化数据交换/数据一致性
Statement: Developed and maintained **RESTful APIs**, optimizing data exchange between financial services, resulting in a **25% reduction** in transaction processing time and improving data consistency by **30%**

**API设计与测试**：用Swagger记录所有端点，Vitest单元测试，Jest/knex.js集成测试 - 使用测试数据库验证从API调用到查询执行再返回的整个流程（例如，发票編輯→更新）。

##### 交易处理时间减少25%
1. 自述
交易处理时间的减少，主要是通过**优化数据交换**来实现的：

首先，我確保了返回的数据结构只包含必要的字段。比如，在发票列表页面，原本接口会返回完整的发票对象，包括一些页面上用不到的字段。我优化后，只返回关键字段（如 initiator/distributor/state 等），提高了接口的响应速度。

其次，我合并了多个原本独立的 API 请求。比方説，原先前端在展示发票详情时，需要分别请求发票信息、留言和用户信息，总共三次调用。我重新设计了一个聚合接口 `/api/invoice/summary/:id`，一次性返回所有需要的数据。这样前端只需发起一次请求，后端也只需一次数据库查询，就降低了网络延迟和系统负担。

在性能指标方面，我记录了后端日志中的响应时长，再进行对比，`发现发票详情页的平均响应时间从大约 800ms 降到了 600ms，结合请求次数减少，`那麽算出整体处理时间缩短了大約 25%。

1. 细节
- 精简 API 返回结构 —— 减少不必要数据传输
	- 搜索頁面返回結果表的時候，只需要展示發票的基礎信息（initiator/distributor/billing party/state/product name)，不需要加載發票的留言記錄
	- 减少字段数量（从几十个字段 → 只保留6个必要字段）；
	- SQL 只查一张表，避免多次联表或多查询；
	- 提高响应速度，降低出错概率（更一致）；
- 合并接口，减少重复调用
	- 以前的做法：
		- 前端先调 `/api/invoice/:id` 拿发票；
	    - 再调 `/api/note/:invoiceId` 拿留言記錄；
		- 再调 `/api/user/:id` 拿留言記錄上的用戶名称。
	- ==> 用户操作一次，发了 **3 个 HTTP 请求**，服务端读取了 **3 次数据库**。
	- 优化方案：
		- 新接口 `/api/invoice/summary/:id` 一次性返回你需要的简明信息：
	- 效果：
		- 一个请求搞定所有数据；
		- 显著减少了网络延迟和后端请求压力；
		- 如果数据库结构清晰，一次 SELECT 比多次 SELECT 更快；
		- **一致性提升**：所有信息来源于一次查询，数据同步性更好。
- 測試：
	- 步骤 1：在后端接口中添加响应时间统计，并将 `duration` 打印到console。
	- 步骤 2：用脚本/Excel/日志分析工具计算平均响应时间
```
// 步骤 1 - invoiceController.ts
export async function getInvoiceSummary(req: Request, res: Response) {
  const start = Date.now();

  try {
    const invoice = await getInvoiceById(req.params.id);
    const comments = await getCommentsForInvoice(req.params.id);
    const user = await getUserForInvoice(invoice.userId);

    const response = {
      invoice,
      comments,
      user
    };

    const end = Date.now();
    console.log(`[INFO] /invoice/summary/${req.params.id} took ${end - start}ms`);
    
    res.json(response);
  } catch (error) {
    console.error(`[ERROR] /invoice/summary failed`, error);
    res.status(500).send("Internal Server Error");
  }
}
```
你可以在控制器或路由层加上 `startTime` 和 `endTime`，并将 `duration` 输出到日志系统（或简单记录在日志文件中做对比分析）。
- **（future）性能25%**：使用JMeter模拟高并发交易，对比优化前后的平均响应时间（如从800ms降至600ms）。
##### 数据一致性30%
1. 自述
为了防止用户重复提交导致的数据不一致问题，我从前后端两方面实现了**幂等性保障**：

在前端，为了避免重复提交，一旦用户点击提交，按钮会立即禁用并显示“处理中”，防止因用户误操作或网络延迟而多次点击。

在后端，我引入了 `request_id` 字段作为请求的唯一标识。如果检测到相同的 `request_id`，系统就会拒绝重复写入，确保数据操作的幂等性。

为验证效果，我们使用了mock工具模拟高频提交，还人工比对线上和备份数据库中的关键记录，看有沒有数据偏差。综合评估后，我们估算数据一致性提升了大约 30%。

1. 细节
**避免重复读写、明确数据来源**
- 加入“幂等性”逻辑（不用事务也能控一致性）
- **问题**：用户可能多次点击“提交”按钮，导致重复写入。
- **解决**：前端禁用按钮，后端使用请求ID去重。
	- 限制前端重复提交（防抖处理)
		- 提交后按钮 `disabled` -> 显示“处理中”状态
	- 基于唯一请求 ID 进行写入去重
		- 每一笔交易或操作请求，可以在客户端或服务端生成一个 `request_id`，用于去重判断。
		- 简单高效，不用用到数据库事务或分布式锁
```
// 假设有个简单的交易处理 API
app.post('/api/transaction', async (req, res) => {
  const { request_id, user_id, amount } = req.body;

  // 步骤 1：检查该 request_id 是否已处理过
  const exists = await db.query(
    'SELECT 1 FROM transactions WHERE request_id = $1 LIMIT 1',
    [request_id]
  );

  if (exists.rowCount > 0) {
    return res.status(200).json({ message: 'Duplicate request ignored' });
  }

  // 步骤 2：执行插入（此处省略验证与业务逻辑）
  await db.query(
    'INSERT INTO transactions (request_id, user_id, amount, status) VALUES ($1, $2, $3, $4)',
    [request_id, user_id, amount, 'pending']
  );

  res.status(201).json({ message: 'Transaction submitted' });
});
```

#### 4 - (DB)数据库重构/减少数据冗余/查询响应时间
Statement: Optimized **SQL** queries and restructured the database schema for the invoice management system, reducing data redundancy by **35%**, cutting query response time by **40%** and boosting invoice retrieval efficiency across **50,000+** products

**DB: MySQL -> PostgreSQL**
- MySQL适合快速开发和高并发应用；PostgreSQL更适合需要稳定性和高级特性的企业应用程序。
- 擅长复杂查询, 优先考虑安全性和标准

##### Data redundancy数据冗余 35%
1. 自述
原本的产品表中嵌入了完整的发票信息字段，包括initiator、distributor、billing party 和区域信息。这种设计在查发票的時候比较方便，但实际运行过程中，我注意到有大量产品共享完全相同的发票信息，导致数据重复率非常高，整个表的体积也很大。

为了解决这个问题，我提出的方案是把这些重复字段抽离出来，重构为一个**billing_patterns 表**，并在产品表中使用外键引用。`这个过程本质上是对数据库进行**第二范式（2NF）规范化。`

重构后，我们通过 `INFORMATION_SCHEMA.TABLES` 和 `INFORMATION_SCHEMA.COLUMNS` 获取各个表的物理存储大小，发现数据库总体体积从约 **500GB** 降到了 **325GB**，大约减少了 **35%** 的冗余数据。

2. 细节
是如何评估和识别出存在数据冗余的问题的？
- （這個公司的發票信息是根據四個因素定義的：initiator，distributor，billing party，和地區。）原先的數據庫設計將發票信息儲存在產品table裏，這樣查詢單個產品的發票信息快。但是發票信息的重複率很高，比如多個產品可能有同樣的發票信息，導致數據庫儲存了重複信息。
**实现方法：**
- **数据库规范化**：将重复存储的字段（如發票改爲billing pattern）拆分到独立表中，通过外键关联（這樣查詢單個產品的發票信息的速度可能會稍微降低？但是也降低了數據冗余）。
- **统一数据源**：为通用数据（如bottle type价格）建立中央引用表，替代多处冗余存储。
**测量方式：**
- **存储空间对比**：通过数据库分析工具（如MySQL的`INFORMATION_SCHEMA`）统计优化前后总数据量（如从500GB降至325GB）。
- **冗余字段审计**：手动或通过脚本扫描表结构，统计重复字段的消除比例。
3. Implementation
步驟 1：創建 `billing_patterns` 表
```
CREATE TABLE billing_patterns (
  id INT AUTO_INCREMENT PRIMARY KEY,
  initiator VARCHAR(255),
  distributor VARCHAR(255),
  billing_party VARCHAR(255),
  region VARCHAR(100),
  UNIQUE KEY uq_billing_pattern (initiator, distributor, billing_party, region)
);
```
步驟 2：將產品表中原本的欄位去重插入新表
```
INSERT IGNORE INTO billing_patterns (initiator, distributor, billing_party, region)
SELECT DISTINCT initiator, distributor, billing_party, region
FROM products;
```
步驟 3：為產品表添加外鍵欄位
```
ALTER TABLE products ADD COLUMN billing_pattern_id INT;
```
步驟 4：關聯對應的 `billing_pattern_id` 到產品表，可以通過 `UPDATE JOIN` 實現
```
UPDATE products p
JOIN billing_patterns bp
  ON p.initiator = bp.initiator
 AND p.distributor = bp.distributor
 AND p.billing_party = bp.billing_party
 AND p.region = bp.region
SET p.billing_pattern_id = bp.id;
```
步驟 5：刪除原來重複的列
```
ALTER TABLE products
DROP COLUMN initiator,
DROP COLUMN distributor,
DROP COLUMN billing_party,
DROP COLUMN region;
```
額外：查看空間節省情況
```
SELECT
  table_name,
  ROUND((data_length + index_length) / 1024 / 1024 / 1024, 2) AS size_gb
FROM information_schema.tables
WHERE table_schema = 'your_database_name'
ORDER BY size_gb DESC;
```
##### Query response time查询时间 40% -> 分页优化
1. 自述
原来的应用在用户搜索时，会把所有符合条件的数据一次性查出来然後返回给前端。数据量大的情況下，应用响应很慢，用户体验也差。所以我设计了一个「前五页预加载 + 之后按需加载」的策略来优化查询性能。

具体做法是这样的：每次用户搜索时，后端只返回前五页的数据（比如每页 20 条，总共 100 条）。这部分数据直接缓存到前端（在 Vue框架的data/state中）。只要用户在这五页内翻页，前端就直接从本地缓存拿数据，不需要再次发请求。
当用户翻到第六页或更后面，前端才会再向后端发起新的分页查询，也是一种「lazy loading」。这样給后端減负，也让用户在大部分情况下能快速拿到结果。

在数据库端，我是用 LIMIT 搭配 OFFSET 来实现分页。虽然 OFFSET 很大时查询效率会变差，不过我有先和 finance 部门确认过，他们大多数操作其实只会在前五页，所以这个策略是符合实际使用行为的。
数据库层面我是用 `LIMIT` 搭配 `OFFSET` 来实现分页。虽然 OFFSET 很大的时候查询效率会变差`（因为数据库仍然要扫描前面所有记录再丢弃）`，但我和finance部门确认了：他们大部分操作都集中在前五页，所以这个方案在实际场景下是非常有效的。

当然我也有考虑过其他优化方式，例如 keyset pagination（基于主键的游标分页）和索引。但是 keyset 分页不太方便跳页；另外，索引的维护成本在我们这种写入频繁的系统中也比较高。

最后为了验证效果，我用 MySQL 的 EXPLAIN (看查了幾行) 和 SHOW PROFILES (看時間) 对比优化前后的查询：`最常见的查询响应时间从原来平均 1.2 秒缩短到 0.7 秒，`由此算出查询效率提升了 40%。

2. 细节
**实现方法：**
- **高效分页策略**：分页优化的核心思路，是**延迟加载（Lazy Loading）+ 限制查询范围（Limit + Offset）**，避免一次性查出全部数据，从而减少数据库的压力和前端加载时间。
	- 每次搜索时，数据库查询只返回**前五页**的内容。例如，每页 20 条记录，五页就是 100 条记录：`SELECT * FROM invoices WHERE 条件 LIMIT 100 OFFSET 0;`
	- 这样用户第一次搜索：只请求前 5 页（100 条）数据，用户快速看到结果，无需等待全部结果加载。
		- 如果用户只在这五页之间翻来翻去，前端就用本地缓存的数据（在 Vue框架的 **data/state** 裡），不重复请求数据库。
	- 用户点到第 6 页或之后：再向后端发起新的请求，比如：`SELECT * FROM invoices WHERE 条件 LIMIT 20 OFFSET 100;`
	- 这属于“**按需加载**”策略，只有用户真的需要，才会加载后续数据。
- 原系统可能在搜索时执行：
	- `SELECT * FROM invoices WHERE 条件;`
	- 这会把所有符合条件的记录都返回，数据量一大就非常慢。优化后通过 LIMIT 控制返回条数，极大减轻数据库负担。
- **弊端：**
	- 数据库仍需扫描整个表才能决定 OFFSET 应该跳过哪些记录，尤其 OFFSET 很大时（比如跳过前 10000 条）非常慢。
		- 数据库**必须从第一条开始扫描（排序后）**，一条一条数到第 10000 条，才能知道从哪里开始取那 20 条。
		- 即使那些 10000 条不返回，也要先从磁盘读出来、经过排序、然后扔掉。
		- 这个「扫描 + 丢弃」的过程在 OFFSET 很大时代价就非常高。
	- 所以即使分页减少了返回数据量，**没索引时查询仍然可能很慢**。
- **高效分页策略2 (未采用)**：**基于上次查询的主键分页（keyset pagination）** 
	- 记录上次的最大ID，下一页从该ID开始查询：`SELECT * FROM invoices WHERE id > 上一页最后一条id LIMIT 20;`
		- 第1页查询：`SELECT * FROM invoices ORDER BY id ASC LIMIT 10;`
			- 前端收到 10 条数据，其中最后一条记录的 ID 是 `105`。
		- 前端再发出第2页请求：
			- `SELECT * FROM invoices WHERE id > 105 ORDER BY id ASC LIMIT 10;`
			- 这就跳过了前面的 105 条数据，而不需要数据库做 `OFFSET 105` 的操作。
- 前端需要**记住上一页最后一条数据的主键 ID**
	- 数据库本身不会记住你上一次查了什么，也不会自动提供“下一页”的 ID。只有前端知道用户上一次拿到的数据中最后一条记录的 ID 是多少。
	- 所以前端要负责：
		- 保存“上一页最后一条数据的 ID”
		- 把这个 ID 传给后端，作为下一页查询的起点
- **弊端1：如果用户跳页（比如從第 1 页点第 10 页），前端要链式计算多次分页的最后 ID**
	- Keyset pagination 是**基于当前位置往前或往后翻页**的，无法直接跳转到“第 X 页”，不像传统分页（OFFSET）那样能指定页码。
	- 所以前端可能需要：
		- 把之前每一页的最后 ID 缓存下来
		- 用户点“第 5 页”时，用“第 4 页最后一条的 ID”作为查询条件
- **弊端2：页面刷新或返回时，前端要重新定位分页状态**
	- 如果用户刷新页面或返回上一页，前端必须能重新定位分页的位置。Keyset pagination 不支持直接从页码定位，所以需要前端存储每一页的分页状态（比如每一页的起始 ID）。
- **高效分页策略3 (未采用)**：为分页排序字段（如时间戳、ID）添加组合索引
	- 在这个项目中，我们之所以没有对所有分页查询字段使用索引，主要出于**数据量规模以及写入频率的考虑**。
	- 系统涉及的数据表体量非常大，包括全美上百万产品的发票数据。如果每个查询字段都建索引，创建和维护成本会很高。我们用了 `LIMIT + OFFSET` 做分页查询，但配合前端做了限制，每次最多只查前五页，这样可以控制查询范围，实际上也明显降低了查询时间，所以不靠索引也能跑得很快：
		- **创建和维护索引的代价非常高**  
			- 对于大表，索引的创建和更新会消耗大量的 CPU 和 IO 资源。尤其是在高频写入（如每天数十万到上百万条发票记录）的场景下，每次插入、更新或删除都会触发索引的重建或调整，这将直接影响整体系统的吞吐性能。
	- 如果要再进一步优化，我会考虑针对高频查询条件做覆盖索引或改用 keyset 分页。
**测量方式：**
- **执行计划分析**：使用数据库工具（如`EXPLAIN`）确认分页查询是否命中索引，避免全表扫描。
- **生产监控**：观察真实用户的分页操作延迟（如通过New Relic的APM指标）。
-  **(future after switch to PostgreSQL) 压测对比**：通过pgBench等工具模拟分页请求，统计优化前后平均响应时间（如从200ms降至120ms）。
3. Implementation
步驟 1：查詢效能分析 - `EXPLAIN`
```
EXPLAIN SELECT * FROM products
WHERE name LIKE '%Coke%'
ORDER BY updated_at DESC
LIMIT 20 OFFSET 100;
```
步驟 2：查詢效能分析 - `SHOW PROFILES`
```
SET profiling = 1;

-- 你要分析的查詢
SELECT * FROM products
WHERE name LIKE '%Coke%'
ORDER BY updated_at DESC
LIMIT 20 OFFSET 100;

-- 查看時間
SHOW PROFILES;
```
#### 5 - (部署)Docker/CI-CD管道/缩短部署时间/100%自动化测试覆盖
Statement: Created and deployed **CI/CD** pipelines using Docker, slashing deployment time by **50%** and ensuring 100% continuous integration and automated testing coverage 

**CI/CD 管道和测试流程：**
- 使用ESLint/Prettier 进行代码质量检查
- 前端 - 我们用`Vitest @vue/test-utils`，对每个组件和功能进行了全面的单元测试，确保了100%的测试覆盖率。
- 后端 - 使用`Jest`和`knex`进行集成测试，测试从API调用到查询执行再返回的整个流程。
	- 首先通过`Docker`启动一个一次性的DB容器。
	- `knex`用來定义数据库的表结构，然后插入测试数据。
	- 然后使用`Jest`运行集成测试，确保了所有API端点正常運作。整个流程都在Docker容器中进行，确保了测试环境的一致性。
- 打包生成Electron安装程序
**缩短50%的部署时间：**  
- 自动化的前端单元测试和後端集成测试缩短了大约50%的部署时间
- 自动化
	- **前端单元测试：**
    - **自动化：** 在CI/CD管道中，使用`npm run test`（一个预先配置的npm脚本）来运行所有前端单元测试。每次提交代码时，CI系统（GitHub Actions）会自动执行这个脚本来运行所有单元测试。
        
	- **后端集成测试：**
    - **自动化：** 在CI/CD管道中，我配置了脚本来自动启动一次性的Docker容器并运行数据库实例。在每次代码推送时，脚本会使用`docker-compose`命令自动启动一个DB容器并插入测试数据。
	    - 测试数据写死为静态Seed文件（提高可重复性和可维护性）

Integration Test Details: [[#Backend Test]]

**Dockerized部署优化**: 使用多阶段Docker (build stage & runtime stage) 构建来分离构建环境和运行时环境, 减少映像大小(image size)和部署时间。
	*Build Stage构建阶段*: 复制包, 安装依赖, 执行build命令→*编译app*
	*Runtime Stage运行阶段*: 从builder阶段复制已构建的app并运行→*运行app*

Docker八股: [[#Docker]]
#### 6 - General Follow-Up
Maintainability & Collaboration (维护和协作)
- Documentation: Maintain architecture diagrams and API interface design.
- TypeScript Practices: Consistent code style (ESLint/Prettier).
- Testing: Unit Test (Vitest - individual modules) and Integration Test (Jest - Ensure DB, IPC and Vue-Electron interactions work as expected ).

未来改进: 
	E2E测试: `Playwright` or `Cypress`
	Kubernetes分阶段部署
	- CI阶段构建app后端服务（例如api，数据库迁移）的Docker镜像后, k8s提取这个image并部署到一个临时pod中进行测试。
	- CD阶段测试通过后, k8s可以提升这个image到一个暂存空间(staging namespace), 最终批准Electron-builder打包app部署。
	- 协调后端服务和数据库的测试环境, 负载测试(load-testing)验证app的性能, 可以确保优化。

## Project - GeneWeaver Backend
### Deep-Dive
#### 1 - (总结)Scrum/Flask/REST API
Developed **REST API** for Jackson Laboratory using **Python** & **Flask** in **Scrum** environments
在Scrum环境中使用Python/Flask为Jackson实验室开发REST API

**Workflow Summary:**
在这个capstone项目中，我主要负责基于**Python和Flask框架**开发REST API。整个开发流程是在**Scrum敏捷开发环境**中进行的，我们的团队由2位后端开发和1位前端开发组成，每个Sprint为期两周。

在每个Sprint开始时，我们会召开Sprint Planning会议，mentor提出需求，我们团队一起拆解任务并估算Story Point。我主要负责实现用户相关功能的REST API，比如**用户注册、登录、查询基因集上传记录等端点**。每次迭代我大约会完成1到2个API端点的设计、编码和单元测试。

举个例子，我实现了一个**基因集上传的POST端点**，用户可以通过这个API上传一个包含基因列表的文件，我在后端使用Flask解析上传内容，做初步校验后调用数据库模块，将数据写入PostgreSQL，并返回上传状态。这个接口同时支持错误处理，例如文件格式不符合时会返回400错误。

在Scrum流程中，我们每天有15分钟的Daily Standup，汇报工作进展和遇到的问题；每个Sprint结束前，我们会进行**Code Review**，通常通过GitHub的Pull Request功能来完成。代码提交前，我会写好对应的**Pytest单元测试**，确保覆盖常见的输入输出场景。

#### 2 - 微服务/更新停机时间
Integrated analytical tools in microservices and mitigated downtime during tool update by 18%
在微服务中集成分析工具，并将工具更新期间的停机时间减少18%

我们将原本耦合在一起的功能模块**拆分为两个独立的微服务**：
- **用户浏览服务（Frontend Service）**：负责页面渲染、用户交互以及静态资源处理；
- **分析服务（Analytics Service）**：处理基因数据分析。
这两个服务通过REST API进行通信，使用HTTP协议交换数据。通过Flask框架可以简便地创建RESTful API，实现服务之间的交互。

此外，两者采用**独立数据库**，分析服务使用 PostgreSQL（适合处理复杂的分析查询），浏览服务最初使用 SQ-Lite，后期迁移到 MySQL（提升了访问性能）。数据库层面的隔离进一步提升了系统的可扩展性和灵活性。
```
**通信机制**
- 在高并发的情况下，我们还引入了 **异步消息队列**（如 Kafka），通过异步事件传递避免了同步通信的延迟，进一步优化了服务的响应时间和可靠性。
- **异步消息队列**：通过 Kafka/RabbitMQ 传递分析事件（如用户点击、页面停留时间）
```
**服务隔离的优势**
- 微服务架构停机时间: 分析工具更新 5分钟（仅分析服务）, 用户浏览功能更新 0分钟（独立部署）

**工具更新时的零停机策略18%**
我们使用以下方式衡量停机时间：
- **部署前后日志比对**：记录每次分析服务更新所需时间（从下线到完全恢复服务）
- **用户体验指标**：重点关注分析工具更新期间，是否有用户反馈分析功能异常或延迟
在引入微服务架构和蓝绿部署之后，我们将分析服务的平均更新停机时间从原本的**约6分钟减少至不到5分钟**，**核心用户浏览服务0停机**，综合计算整体系统对用户影响的**停机时间下降了约18%**。

蓝绿部署（Blue-Green Deployment）
- **并行环境**：分析服务 v1（旧版本）和 v2（新版本）在独立环境中同时运行
- **流量切换**：借助Kubernetes 的服务路由机制，逐步将部分请求切换到新版本，确保新服务稳定后再进行完全切换
- **API 版本控制**：提供版本号明确的 API 接口，避免更新过程中对前端服务造成影响。
```
GET /api/v1/analytics   → 旧版分析工具
GET /api/v2/analytics   → 新版分析工具
```

#### 3 - PostgreSQL/SQ-Lite
Developed backend business logics including user authentication/sign-on and gene set upload; Performed data insertion and retrieval with **PostgreSQL** and **SQ-Lite**
开发后端业务逻辑，包括用户认证/登录和基因集上传；使用PostgreSQL和SQ-Lite进行数据的插入和检索

**Why PostgreSQL and SQ-Lite**
首先，**PostgreSQL**是一个功能强大的关系型数据库系统，我选择它主要是因为它支持复杂的查询、事务处理和数据一致性。在项目中，PostgreSQL主要用于处理更复杂的业务逻辑和大规模的数据存储。例如，用户认证和基因集上传的业务逻辑需要存储大量的结构化数据，且要求高并发和高可靠性，PostgreSQL在这方面表现非常好。

而**SQ-Lite**则是在一些轻量级的需求中使用的，它作为开发环境的快速替代，使用SQ-Lite既能提高性能，也能减少数据库管理的复杂度。

在实际操作中，我使用了SQL语句进行数据的插入和检索。例如，在PostgreSQL中，我编写了复杂的查询来检索基因集的相关信息，并确保在插入数据时能够进行完整性检查；而在SQ-Lite中，更多的是用于快速的数据存取，减少了查询的复杂度。

#### 4 - Async Python/页面缓存/HTTPS/web验证
Optimize runtime performance on concurrent tasks using **Async** Python and recurrent analytical queries using **Page Caching**; Implemented secure data access point using HTTPS protocols & web authentication
使用Async Python优化并发任务的运行时性能，并使用页面缓存优化循环分析查询；使用HTTPS协议和web身份验证实现安全数据接入点

**如何使用Async Python优化并发任务的运行时性能？：**
1. 使用asyncio处理基因数据分析任务
	1. 用户提交分析请求 → 任务加入队列 → 立即返回“处理中”状态  
	2. 后台异步执行分析 → 用户可继续浏览其他页面  
	3. 分析完成后通过WebSocket/Polling通知用户  
```
import asyncio

async def analyze_data(task_id):
    # 假设这段代码需要进行复杂的I/O操作，如数据库查询
    data = await fetch_data_from_db(task_id)
    result = process_data(data)
    await store_result_in_db(result)
    return result

async def fetch_data_from_db(task_id):
    # 异步数据库查询
    await asyncio.sleep(2)  # 模拟数据库查询
    return "data"

async def main():
    task_id = 123
    result = await analyze_data(task_id)
    print(f"Analysis Result: {result}")

asyncio.run(main())
```
1. **事件循环机制**：通过`asyncio`的事件循环，所有I/O操作都在单线程下并发执行，避免了线程切换的开销，大大提高了并发性能。
	1. 单线程处理数千并发任务
	2. I/O等待时间（如数据库查询）可被其他任务利用
2. **用户体验优化**
	1. **进度反馈**：实时显示分析进度条
	2. **中断恢复**：允许用户暂停/取消分析
	3. **后台运行**：即使用户关闭页面，分析仍持续进行
- (future) CPU密集型任务改用Celery+Redis
```
async def send_progress(progress):
    # 通过WebSocket向前端发送实时进度
    await websocket.send(f"Progress: {progress}%")
```

**页面缓存**：
页面缓存主要用于减少频繁的重复查询，提升系统响应速度。在此项目中，我使用了双重缓存机制：
1. **双重缓存机制** 
	1. **浏览器缓存**：使用`SessionStorage`存储用户设备本地的历史分析结果，减少重复加载的时间。
	2. **服务器缓存**：使用LRU在服务器端 (存储在服务器内存RAM中)保存高频查询的分析结果。
	3. **协同工作**：用户提交分析请求时，先检查本地缓存，如果命中则直接显示结果；如果没有命中缓存，则向服务器请求结果，获取后存入缓存并显示。
2. **识别重复查询**
	1. 用户提交分析参数 → 生成唯一缓存键（如MD5哈希） → 匹配历史记录
3. **本地存储策略**
	1. **SessionStorage**：临时保存当前会话的分析记录
4. **服务器端内存缓存优化**
	1. **LRU算法**：保留最近使用的1000条分析结
	2. **分层存储**：
		1. 热数据：驻留内存（TTL=10分钟）
		2. 温数据：持久化存储（TTL=24小时）
5. **缓存更新流程**
	1. 用户发起新分析 → 检查本地缓存 → 命中则直接渲染 → 未命中则请求服务器 → 服务器返回数据 → 存储到本地 → 显示结果
6. 缓存更新策略 - **主动失效**
	1. 用户logout → 清除相关分析缓存
	2. 定时夜间刷新热点缓存
7. (Future: )Redis缓存热门基因查询结果

**HTTPS** = HTTP + TLS加密层
- 全站HTTPS -> 从Let's Encrypt获取免费证书 -> 配置证书自动续期（每90天） -> 在Web服务器（如Nginx）中启用TLS 1.2/1.3

**Web身份验证**
1. **登录阶段**：
    - 用户提交凭证（用户名/密码）
    - 服务端验证后生成签名令牌（JWT, 有效期2小时）
    - 令牌包含用户ID、权限和有效期
2. **访问阶段**：
    - 客户端在Authorization头携带JWT令牌
    - 服务端验证令牌签名和有效期
    - 拒绝无效/过期令牌
3. 定期执行OWASP ZAP安全扫描
## Project - eCommerce Platform
### Tech Stack
#### Testing & Deployment
##### E2E Test & CI/CD
- Tool: Postman
	- 通常用于API测试，但也可以通过模拟跨多个API调用的用户工作流来用于E2E测试
	- 测试从用户注册→登录→产品浏览→购物车管理→结帐→付款处理的整个流程。
- Automating**自动化** E2E Tests with Postman
	- **Integration with CI/CD (Heroku)** 
Developer更新代码→触发Heroku CI→启动一个临时测试dyno（隔离环境）→部署到这个dyno→运行单元测试 (轻量级API检查)和集成测试 (验证MongoDB/Redis交互)→测试通过→部署到staging→运行`npm test` (完整的E2E验证)→Newman执行Postman collection。
	1. 如果测试通过→人工审批→投入生产环境。
	2. 如果测试失败→Slack Alert+阻止部署。
- Limitation: 
	- No UI Testing, as Postman only tests APIs. 
	- Complex Workflows for multi-step scenarios.
- Future Improvement
	- Parallelize Test并行测试 in 临时测试dyno
		- API Unit Tests on single functions/modules using Postman
		- Fast Smoke Tests on critical user flows
	- Staging: Full E2E validation using **Cypress**
	- **Heroku CI→启动一个临时测试dyno→运行单元测试→通过后运行Smoke Test→部署到staging→运行E2E测试→通过后人工审批→投入生产环境**
	
CI/CD Implementation
1. In Postman, group all E2E tests (e.g., `Auth`, `Orders`, `Stripe`) into a **Collection**, then export it as a JSON file
	1. 分组到一个“集合”中, 导出为JSON文件
	2. 导出环境变量, 确保每个请求都有Postman Test (Assertions)
2. Set Up Heroku CI/CD
	1. Heroku链接GitHub, 启用自动部署。
	2. **Heroku CI**: configure `app.json` to define test script
3. **Automate** E2E Testing with Newman
	1. Newman: Postman’s CLI tool to run collections
	2. 配置Heroku运行测试 (`npm test`)
4. Configure Heroku **Pipeline**
	1. Staging Environment (生产环境的副本, 用于最终测试)
		1. Automatically deploy branches (e.g., `staging`) and run E2E tests
		2. 自动部署分支（例如“暂存”）并运行端到端测试。
	2. Production Environment (真实的用户交互的实时系统)
		1. Manually promote from staging after tests pass
		2. 在测试通过后**手动**触发把应用交付到生产环境。

Postman E2E Workflow
1. 设置Collections和环境
	1. Collections: Group related API requests
	2. Environment Variables: like base_url, JWT token after login, order_id during the checkout
2. 测试Authentication Flow认证流程
	1. Register User
		1. Send: `{ "email": "test@example.com", "password": "123456" }`
		2. Save `response.body.token` to `{{token}}`.
	2. Login User
		1. Send credentials (凭据), extract & store the new JWT token (JWT令牌)
3. 测试获取产品和购物车流程
	1. Fetch产品
		1. URL: (`GET /api/products`)
		2. Verify response contains product list
	2. 添加到购物车
		1. Send: `{ "productId": "123", "quantity": 2 }`
		2. Headers: `Authorization: Bearer {{token}}`
		3. Test: Check if cart is updated
4. 测试Checkout & Payment (Stripe)
	1. 创建订单
		1. URL: (`POST /api/orders`)
		2. Send cart details, store `orderId` in `{{order_id}}
	2. Mock Stripe支付
		1. Send: `{ "orderId": "{{order_id}}", "token": "stripe_test_token" }`
		2. Test: Verify payment success response
5. Validate订单
	1. URL: (`GET /api/orders/{{order_id}}`)
	2. Test: Check if status is `completed`

### Deep-Dive
#### 1 - (总结)REST API
Built up a **MERN** stack-based eCommerce platform; Developed and maintained software features to enhance customer engagement through front-end **UI** components, REST API services, and data modeling
搭建基于MERN的电子商务平台；开发和维护软件功能，通过前端UI组件、REST API服务和数据建模来增强客户参与度

#### 2 - 状态管理/MongoDB/Redis
Designed data model using **MongoDB**; integrated **Mongoose** for query searching performance enhancement and **Redis** for schema definition; Leveraged **JWT** for API authentication and **Redux** Toolkit for state management
MongoDB设计数据模型；集成了Mongoose提高查询搜索性能以及Redis定义schema；JWT用于API认证，Redux工具箱用于状态管理

#### 3 - E2E端到端/Heroku/CI/CD
Applied **Postman** for end-to-end testing and **Stripe** API for payment; Utilized **Heroku** for deployment & CI/CD pipeline for smooth deployment and continuous integration 
Postman用于端到端测试，Stripe API用于支付；使用Heroku进行部署和CI/CD管道

## Project - SpringBoot Platform
### Workflow
1. **数据采集层**
    - 从数据源（流式Stream API: 如Twitter的Firehose API，YouTube Live Streaming API，支持持续推送数据）实时抓取流行趋势原始数据
    - 通过Kafka建立高吞吐事件流管道，持续传输视频的观看量、点赞量等核心指标
	    - 作为消息中间件，Kafka接收流式API的数据并缓冲，将实时数据的生产和消费分离(解耦生产者和消费者)，确保高并发下的可靠性。
		    - **数据到达后，app不直接处理**，而是将其作为**生产者**发送到Kafka的指定Topic（如`tweets-topic`）。
		    - Kafka的Topic按分区存储数据，支持多消费者并行处理。
2. **数据处理层**
    - Spring Boot后端服务接收Kafka流数据
	    - 通过内置的Kafka支持（如`Spring Kafka`库），简化流式API与Kafka的集成。
	    - Spring Boot的另一服务作为**Kafka消费者**，订阅Topic（如`tweets-topic`）并处理数据（如存储到数据库）。
    - Spring Boot实时计算视频热度排名（基于观看量+点赞量）
    - 使用Redis缓存当前热门趋势结果，减少重复计算和MySQL查询
3. **数据存储层**
    - MySQL持久化存储：
        - 用户配置(订阅关系)
        - 记录历史趋势数据
        - 事务性管理通知日志
    - Redis缓存：
        - 分布式锁控制热门榜单更新
        - 高频访问的实时趋势数据
4. **服务交付层**
    - Nginx + Apache：
        - 将动态生成的趋势页面转换为静态HTML
        - 通过负载均衡和缓存策略实现毫秒级加载
    - 通知系统：
        - 基于MySQL存储的订阅关系触发推送
        - 与第三方服务（邮件）集成

### 流式Stream API
- 支持持续实时推送数据
	- 不间断地从服务器传输到客户端，**无需客户端反复发起请求**。
	- 例如Twitter的Firehose API，YouTube Live Streaming API
- **长连接机制**
	- 通过**HTTP长轮询（Long Polling）**、WebSocket或SSE（Server-Sent Events）等技术维持连接，避免频繁建立/断开连接的开销。
- 高效性
	- 客户端无需反复轮询（Polling）检查新数据，减少冗余请求，节省带宽和服务器资源。
- 数据连续性
	- 数据以“流”的形式分块（Chunk）传输，可处理无限序列（如视频流、日志流）。

#### 长连接机制详解
在实时数据传输场景中，长连接机制是流式API实现`持续推送`的核心技术手段。其目的是避免客户端反复建立/断开连接带来的性能损耗，同时保证数据的低延迟。

1. HTTP长轮询（Long Polling）
	1. 原理：
		1. 客户端发起一个HTTP请求后，**服务器不立即响应**，而是保持连接挂起（Hang）。
		2. 当服务器有新数据时，才返回响应并关闭连接；客户端收到后立即发起新的请求，循环往复。
	2. 特点：
		1. 兼容性强：基于标准HTTP协议，无需额外协议支持。
		2. 伪实时：仍有轻微延迟（取决于服务器数据生成速度）。
		3. 资源占用：大量挂起请求可能消耗服务器资源。
	3. 典型应用：早期Web聊天室、股票价格更新等对实时性要求不极端的场景。
2. WebSocket
	1. 原理：
		1. 客户端与服务器通过一次HTTP握手**升级为全双工TCP长连接**，之后双方可随时主动发送数据。
		2. 连接建立后，数据传输**无需HTTP头开销**，直接以二进制或文本帧通信。
	2. 特点：
		1. 真实时：双向通信，延迟极低（毫秒级）。
		2. 高效：无冗余Header，节省带宽。
		3. 复杂度高：需服务器和客户端显式维护连接状态（如心跳包防断开）。
	3. 典型应用：在线游戏、实时协作工具（如腾讯文档）、高频金融交易系统。
3. SSE（Server-Sent Events）
	1. 原理：
		1. 基于HTTP协议，服务器通过**单向持久连接**向客户端推送数据（仅Server→Client）。
		2. 数据格式为简单的文本流（如`data: {...}\n\n`），客户端通过`EventSource` API解析。
	2. 特点：
		1. 轻量级：无需复杂协议，兼容HTTP/2。
		2. 自动重连：客户端内置连接恢复机制。
		3. 单向限制：仅支持服务器推送，客户端需通过其他渠道（如HTTP）提交请求。
	3. 典型应用：新闻推送、实时日志监控、社交媒体Feed更新（如微博新消息提醒）。

#### 流式API vs REST API
- 流式API: 服务器主动推送, 实时性高（毫秒级延迟）, 长连接（持续开放）, 适用流媒体
- REST API: 客户端主动请求, 实时性低（依赖轮询频率）, 短连接（请求-响应后断开）, 适用静态数据获取

#### 流式API与Kafka在Spring Boot中协作
流式API负责实时数据采集，Kafka负责高吞吐量(high throughput)的消息缓冲与分发，而Spring Boot作为集成框架协调整个流程。

### Deep-Dive
#### 1 - (总结)
Developed and launched a web application for displaying popular trends from various sources using Java under the Spring Boot framework in Agile development cycles
在敏捷开发周期的Spring Boot框架下，使用Java开发并启动了一个web应用程序，显示从多个数据源（[[#流式Stream API]]: 社交媒体、视频平台等）实时抓取的流行趋势

1. **系統设计**：
	1. 采用 **发布-订阅模式**，通过Kafka作为消息总线集成多数据源（社交媒体、视频平台）。
	2. 每个数据源对应独立的Kafka Producer，后端Spring Boot服务作为消费者订阅Topic，实时解析数据并计算热度（如观看量×0.7 + 点赞量×0.3）。
	3. 使用 **观察者模式** 动态更新前端：当Redis中热度排名变化时，通过WebSocket主动推送至客户端。
2. **数据一致性保障**：
	1. **统一时间戳**：所有数据源上报时间强制转换为UTC时区，避免时区差异。
	2. **数据去重**：为每条趋势生成唯一ID（如`平台ID+内容哈希`），通过Redis的`SETNX`命令去重。
	3. **最终一致性**：允许短暂延迟（如1秒），通过定时任务补偿缺失数据。
3. **限流与节流**：
	1. 对第三方API调用使用 **令牌桶算法**（通过Guava RateLimiter），限制每秒请求数（如100 QPS）。
	2. 对突发流量启用 **降级策略**：当数据源不可用时，返回缓存的历史趋势并标记为“待更新”。

**Test Plan**
1. **准确性与实时性测试**：
	1. **影子流量**：将生产环境流量复制到测试环境，对比新旧系统输出结果的一致性。
	2. **时间敏感测试**：注入带未来时间戳的数据，验证系统是否按预期丢弃或暂存。
2. **自动化测试**：
	1. **API测试**：Postman的Collection Runner可以用于批量测试
3. **延迟优化**：
	1. 使用 **分布式追踪**（SkyWalking）定位慢链路，如发现Kafka Consumer反序列化耗时高，改用Protobuf替代JSON。
	2. 前端启用 **分块加载**：优先渲染首屏趋势，异步加载后续数据。

#### 2 - Kafka
Implemented event streaming service using Kafka to transmit top trending videos based on views and kudos
通过Kafka建立高吞吐事件流管道，持续传输视频的观看量、点赞量等核心指标

- Spring Boot后端服务接收Kafka流数据
- 实时计算视频热度排名（基于观看量+好评度加权算法）
- 使用Redis缓存当前热门趋势结果，减少重复计算和数据库查询
Kafka八股: [[#Kafka]]

**Streaming & Data Processing**: **数据流入Kafka → 实时计算 → 背压处理**
1. **Kafka高吞吐配置**：
	1. **目标**：高效接收海量视频事件（播放、点赞、分享）。
	2. **分区策略**：按视频ID哈希分区，确保同一视频的事件顺序性。
	3. **按视频ID哈希分区**：
		1. 每个视频的事件（如播放、点赞）根据其ID的哈希值，分配到固定分区。
		2. **作用**：确保同一视频的所有事件在同一分区内**顺序处理**（如先播放后点赞，顺序不乱）。
	4. **生产者批量提交优化**：
		1. **linger.ms=100**：生产者等待最多100ms，将多个事件打包成一个批次发送，减少网络请求次数。
		2. **batch.size=64KB**：当批次大小达到64KB时立即发送，避免内存占用过高。
		3. **效果**：相比单条发送，吞吐量提升30%（如从5万/秒 → 6.5万/秒）。
	5. **分区数设定**：
		1. 根据吞吐量预估设置分区数（如10个分区，每秒处理10万事件）。
		2. 分区数过多会导致Consumer资源浪费，过少则成为瓶颈。
2. **Kafka Consumer消费数据**：
	1. 每个Consumer实例订阅一个或多个分区，按顺序拉取事件。
	2. 消费者组：横向扩展多个Consumer，分摊负载（如3个Consumer处理10个分区）。
3. **排名算法设计**：
	1. 热度公式：`热度 = 播放量(評論) × 0.6 + 点赞量 × 0.3 + 分享量 × 0.1`，权重基于业务调研（用户调研显示播放量最重要）。
	2. **公平性验证**：
		1. A/B测试：对照组使用旧算法，实验组用新算法，统计用户停留时长（新算法组提升15%）。
		2. 长尾保护：对小众视频（播放量<1000）单独加权，避免头部视频垄断榜单，提升内容多样性。
4. **结果缓存与更新**：
	1. **Redis存储结构**：
		1. 使用Sorted Set（有序集合）存储视频ID和热度值，自动按热度排序。
		2. Key示例：`trending:videos:20231101`，Value：`{video_123: 9500, video_456: 8700}`。
	2. **更新策略**：
		1. 每10秒将Kafka消费的最新数据批量更新到Redis，减少频繁写操作。
5. (future) **背压处理**：
	1. Consumer端监控处理延迟，超过阈值时动态扩容Kafka Consumer实例。
	2. 启用 **死信队列**（Dead Letter Queue）暂存无法及时处理的消息，避免雪崩。
	3. **背压检测**：
		1. **监控指标**：
			1. **Consumer Lag**：Kafka消息积压量（未处理消息数），通过Prometheus监控。
			2. **处理延迟**：从事件产生到写入Redis的耗时（如>500ms触发告警）。
		2. **动态扩容**：
			1. 当Lag持续增长超过阈值（如1000条），自动扩容Kafka Consumer实例（如从3个→5个）。
	4. **死信队列（DLQ）处理**：
		1. **场景**：遇到无法处理的异常事件（如数据格式错误、依赖服务超时）。
		2. **流程**：
			1. 将异常消息转发至独立的DLQ Topic（如`dead_letter_video_events`）。
			2. 后续由人工或离线任务分析DLQ数据，修复后重新注入主流程。
		3. **作用**：避免异常消息阻塞主流处理，保障系统持续运行。
	5. **降级策略**：
		1. **缓存兜底**：当Redis更新失败时，返回上一次成功缓存的热榜数据。
		2. **限流**：当Kafka吞吐量达到上限，丢弃低优先级事件（如历史视频的播放事件）。

**Test Plan**
1. **端到端测试**：
	1. 使用 **Kafka Testcontainers** 模拟完整管道：生产者→Kafka→消费者→Redis。
	2. 注入乱序消息（如时间戳倒序），验证排序逻辑健壮性。
2. **数据完整性监控**：
	1. 通过Kafka的`__consumer_offsets` Topic监控Lag，设置报警阈值（如Lag>1000）。
	2. (future) 使用Prometheus统计Redis缓存命中率，低于95%时触发缓存预热。

#### 3 - Redis/分布式锁
Incorporated Redis cache into backend service for distributed lock and query reduction
将Redis缓存集成到后端服务中，用于分布式锁和查询减少

Redis: Caches computed trends from Kafka output
缓存Kafka输出的计算趋势
MySQL: Stores historical trends from Kafka streams
存储Kafka流的历史趋势
Nginx: Serves static trend pages generated from Kafka-fed data
提供从kafka提供的数据生成的静态趋势页面

- Redis缓存：
    - 分布式锁控制热门榜单更新并发
    - 高频访问的实时趋势数据

**分布式锁选型**：
    - 选择Redis而非ZooKeeper，因更低的延迟（亚毫秒级）和更高的吞吐量（10万+ QPS）。
    - 使用Redisson的`RLock`实现可重入锁，避免死锁。

**分布式锁**
**场景示例**：防止同一视频被多个线程重复计算热度。
1. **加锁流程**：
    - **唯一标识**：使用视频ID作为锁的Key（如`lock:video:123`）。
    - **非阻塞获取**：通过`SETNX`命令（SET if Not eXists）尝试加锁。
    - **超时机制**：设置锁的TTL（如10秒），避免死锁，即使客户端崩溃也能自动释放。
2. **解锁流程**：
	1. **Lua脚本原子操作**：确保只有锁持有者能释放锁。
3. **锁竞争优化**：
	1. **分段锁**：将热门资源拆分为多个子锁（如`lock:video:123:part1`），减少争用。
	2. **重试策略**：获取锁失败时，随机退避（如50ms~200ms）后重试，避免雪崩。

**查询减少的缓存策略**
**场景示例**：缓存视频热度排行榜，减少MySQL查询。
5. **缓存逻辑**：
    - **读路径**：
        - 先查Redis，命中则直接返回。
        - 未命中则查MySQL，回填Redis并设置TTL（如60秒）。
    - **写路径**：
        - 更新MySQL后，同步删除或更新Redis缓存（双写一致性）。
6. **缓存数据结构**：
    - **Sorted Set**：存储实时排行榜（Key: `trending:videos`, Value: `{video_123: 9500, video_456: 8700}`）。
    - **Hash**：缓存用户会话信息（Key: `user:session:456`, Value: `{name: "Alice", last_login: "2023-11-01"}`）。
7. **效果验证**：
    - **监控指标**：缓存命中率（>95%）、数据库QPS下降（如从5000 → 800）。
    - **工具**：通过Redis的`INFO`命令或Prometheus监控。

#### 4 - Apache/Niginx/MySQL
Designed a backend notification system and stored data into MySQl database;  Constructed a static HTML converter using Apache and Nginx with minimized loading time
设计后端通知系统，并将数据存储到MySQl数据库中；构建一个静态HTML转换器使用Apache和Nginx与最小的加载时间

- MySQL持久化存储：
    - 用户订阅关系
    - 历史趋势数据
    - 通知系统日志
- Nginx + Apache：
    - 将动态生成的趋势页面转换为静态HTML
    - 通过负载均衡和缓存策略实现毫秒级加载
- 通知系统：
    - 基于MySQL存储的订阅关系触发推送
    - 与第三方服务（短信/邮件）集成

**后端通知系统设计（MySQL）**
**场景示例**：向用户推送系统通知（如视频审核结果）。
1. **MySQL表设计**：
    - **读写分离**：写操作主库（InnoDB事务支持），读操作从库（MyISAM查询优化）。
    - **表结构核心字段**：
```
CREATE TABLE notifications (  
  id BIGINT PRIMARY KEY AUTO_INCREMENT,  
  user_id INT NOT NULL,         -- 接收用户  
  content TEXT NOT NULL,        -- 通知内容  
  status ENUM('pending', 'sent', 'failed') DEFAULT 'pending',  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
  INDEX idx_user_status (user_id, status)  -- 加速查询未发送通知  
);  
```
2. **可靠性保障**：
    - **重试机制**：对失败通知（如第三方推送服务超时）最多重试3次，间隔指数退避（1s → 5s → 25s）。
    - **死信队列**：最终失败的通知归档到S3，供人工排查（如错误日志、错误码）。
3. **性能优化**：
    - **批量处理**：每次从MySQL拉取100条`pending`通知，批量发送。
    - (future) **异步处理**：通过消息队列（如RabbitMQ）解耦通知生成与发送。

**静态HTML转换器（Apache/Nginx优化）**
**场景示例**：将动态生成的视频详情页预渲染为静态HTML，加速访问。
1. **静态化流程**：
    - **触发时机**：当视频发布或更新时，后台服务调用渲染引擎生成HTML文件。
    - **存储路径**：按视频ID分目录存储（如`/html/videos/123/index.html`）。
2. **Web服务器优化**：
	- **Apache辅助**：用于处理少量动态请求（如用户登录），通过`mod_rewrite`将静态请求路由到Nginx。
3. **性能提升效果**：
    - **加载时间对比**：动态页平均800ms → 静态页200ms（减少75%）。
    - **工具验证**：通过Lighthouse测试，性能评分从60提升至90+。

## Python
### 装饰器Decorator
- 是一个函数，用来“包装”另一个函数，从而在不改变原函数代码的前提下，给它添加额外功能。
- 有时候我们希望在多个函数中重复做一些“通用的事情”，比如： 打印日志, 测试运行时间。
- 我们不想每次都手动复制粘贴这些逻辑，所以就可以用装饰器来“自动地”加在函数前后。
```python
def sample_decorator(func):
    def wrapper(*args, **kwargs):
        print("调用函数之前")
        func(*args, **kwargs)
        print("调用函数之后")
        return result
    return wrapper

@sample_decorator  # 相当于 `say_hello = my_decorator(say_hello)`
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("World")
```

### 怎么写private私有变量/保护变量
- Python并没有像 Java 或 C++ 那样真正意义上的“私有变量”。  
- 但是，Python 提供了一种**命名约定**来表示变量是“私有的”，也就是说，**不建议在类的外部直接访问它**。
```python
class Person:
    def __init__(self, name, gender, age):
        self.name = name        # 公有变量
        self._gender = gender   # 保护变量
        self.__age = age        # 私有变量: 在变量前面加上两个下划线 `__`，来表示这个变量是私有的。

    def get_age(self):
        return self.__age

p = Person("Alice", "F", 10)
print(p.name)         # 可以访问
print(p._gender)      # 虽然能访问，但不建议在外部用
print(p.__age)        # 会报错！AttributeError
# 这个时候直接访问 `__age` 是不被允许的，因为 Python 会进行**名称改写（name mangling）**，其实它会变成 `_Person__age`。
print(p._Person__age)  # 还是能“强行”访问（不推荐）
```
## Java
### 死锁以及如何避免
两个或多个线程在运行过程中，**因为争夺资源而互相等待**，导致所有线程都无法继续执行的情况。

比如説，线程 A 拿到了资源 1，想要获取资源 2；线程 B 拿到了资源 2，正好也想获取资源 1；结果两个线程都在等待对方释放资源，就进入了死锁状态。

**死锁发生的四个必要条件：**
1. 互斥条件：资源一次只能一个线程用
2. 占有并等待：拿着自己的资源，还想要别人的(两人都不肯退)
3. 不可抢占：资源不能被强行抢走(释放)，只能被占用线程主动释放
4. 循环等待：两个或多个线程形成资源的循环等待链 (A等B，B等A)

**只要打破其中一个条件，就可以避免死锁。：**
1. **资源排序法**：按固定顺序申请资源
    给所有资源定义一个固定的获取顺序，线程必须按照这个顺序去申请资源，避免形成循环等待。
2. **一次性申请所有资源**：一次申请所有需要的资源
    如果线程需要多个资源，必须一次性申请完，拿不到就全部释放，稍后重试。
3. **使用 `tryLock()` 等带超时的方法**：等太久就放弃重试
    像 `ReentrantLock` 提供了 `tryLock(long timeout)` 方法，线程在一定时间内拿不到锁就放弃，从而避免一直等待。

### final, finally 和 finalize 的区别
**`final` 是一个关键字，用于声明"不可更改"的内容。**
- 如果用在变量上，表示这个变量是常量，一旦赋值就不能再修改。
- 如果用在方法上，表示这个方法不能被子类重写。
- 用在类上，则表示这个类不能被继承。  
    它的主要作用是提供不可变性和安全性。
**`finally` 是和 `try-catch` 异常处理结构配合使用的。**
- 不管是否发生异常，`finally` 块里的代码都会被执行。
- 它常用于释放资源，比如关闭文件流、数据库连接等，确保资源不会泄露。  
    这部分对程序的健壮性和资源管理非常关键。
**`finalize` 是 `Object` 类里的一个方法，主要用于垃圾回收前的清理操作。**
- 当垃圾回收器准备回收一个对象时，会调用它的 `finalize()` 方法。  
    不过这个方法不推荐手动使用，因为它的调用时机不确定，而且在 Java 9 之后也被标记为“过时”，更推荐使用 `try-with-resources` 或者显式的资源释放方式。

### 静态变量和实例变量
**静态变量**
静态变量是用 `static` 关键字修饰的，属于**类本身**，而不是与类的实例（对象）关联。
- 内存在类加载时分配，
- 所以它在**类加载时就会被创建**，在内存中只有一份`(在方法区中的静态区)`，所有对象共享同一个静态变量。
- 生命周期与类相同(程序运行期间)
**实例变量**
实例变量属于类的实例(对象)，必须通过对象实例访问，每个实例拥有独立的副本。
-  每创建一个对象，实例变量就会被初始化一次`(在堆内存中的对象内部)`，**互相之间互不影响**。
- 生命周期与与对象实例相同(对象被回收时销毁)

### 静态变量和静态方法
在Java中，静态变量和静态方法是与类本身关联的，而不是与类的实例（对象）关联。它们在内存中只存在一份，可以被类的所有实例共享。

**静态变量**: 在类中使用 `static` 关键字声明的变量，它们属于类而不是任何具体的对象。
1. **共享性**：所有**该类的实例共享同一个**静态变量。如果一个实例修改了静态变量的值，其他实例也会看到这个更改。
2. **初始化**：静态变量在类被加载时初始化，只会对其进行一次分配内存。
3. **访问方式**：静态变量可以直接通过类名访问，也可以通过实例访问，但推荐使用类名。
4. **使用场景**：常用于需要在所有对象间共享的数据，如计数器、常量等。
```
public class MyClass {
    static int count = 0;   // 静态变量

    public MyClass {count++;    // 每创建一个对象，静态变量自增}

    public static void printStaticVar() {System.out.println("Static Var: " + count);}
}

// 使用示例
MyClass obj1 = new MyClass();
MyClass obj2 = new MyClass();
MyClass.printStaticVar();  // 输出 Static Var: 2
```

**静态方法**: 在类中使用 `static` 关键字声明的方法，也属于类而不是任何具体的对象。
1. **无实例依赖**：静态方法可以在没有创建类实例的情况下调用。对于静态方法来说，不能直接访问非静态的成员变量或方法，因为静态方法没有上下文的实例。
2. **访问静态成员**：静态方法可以直接调用其他静态变量和静态方法，但不能直接访问非静态成员。
3. **多态性**：静态方法不支持重写（Override），但可以被隐藏（Hide）。
4. **使用场景**：常用于助手方法（utility methods）、获取类级别的信息或者是没有依赖于实例的数据处理。
```
public class MyClass {
    static int count = 0;   // 静态变量

    // 静态方法
    public static void incrementCount() {count++;}

    public static void printStaticVar() {System.out.println("Static Var: " + count);}
}

// 使用示例
MyClass.incrementCount();   // 调用静态方法
MyClass.printStaticVar();   // 输出 Static Var: 1
```

### 静态方法和实例方法
静态方法（Static Method）和实例方法（Instance Method）的核心区别在于：**是否依赖对象来调用，以及能否访问类的成员变量。**

**静态方法（static method）**
- 使用 `static` 关键字修饰
- **属于类本身**，不属于任何具体对象
- 可以 **不创建对象就调用**，比如：`ClassName.methodName()`
- **不能访问实例变量或实例方法**，因为它没有 `this` 引用
- 常见于工具类，比如 `Math.abs()`、`Collections.sort()` 等

**实例方法（非 static 方法）**
- 不使用 `static` 修饰
- **属于对象**，必须先创建实例（new 对象）才能调用
- 可以访问类中的**实例变量**和**其他实例方法**
- 适用于依赖对象状态的方法

### ArrayList和LinkedList
数据结构方面：
- ArrayList：内部使用动态数组存储数据。因此，它支持随机访问，通过索引访问元素非常快，比如 `get(index)` 是 O(1) 的时间复杂度。  
	- 但是如果涉及到中间插入或删除元素，就比较慢了，因为后面的元素需要**整体移动**，插入/删除是 O(n)。
- LinkedList：内部使用双向链表存储数据。这使得在列表的开头或结尾插入、删除元素非常快，时间复杂度为O(1)。  
	- 但查找元素，比如 `get(index)`，需要一个个往后找，时间复杂度是 O(n)。

性能方面：
- ArrayList：添加元素时如果需要扩容（即当前数组已满），则需要复制原数组到新的更大的数组，这样的操作时间复杂度为O(n)。
- LinkedList：每个节点还需要额外存前后指针，内存开销更大。

### HashMap和ConcurrentHashMap
Source: https://xiaolincoding.com/backend_interview/internet_giants/elme.html#%E8%AE%B2%E4%B8%8Bhashmap
**HashMap**
HashMap 数据结构是数组和链表，HashMap通过哈希算法将元素的键（Key）映射到数组中的槽位（Bucket）。如果多个键映射到同一个槽位，它们会以链表的形式存储在同一个槽位上，所以冲突很严重，一个索引上的链表非常长，效率就很低了 - O(n)。

**JDK1.8**: 当一个链表的长度超过8的时候就转换数据结构，使用**红黑树**，查找时使用红黑树，时间复杂度O（log n），可以提高查询性能，在数量较少时(<6)，会将红黑树转换回链表。

- 线程不安全 - 同时往车里放商品，可能导致：数据丢失, 数据覆盖, 死循环

**ConcurrentHashMap**
使用数组加链表的形式实现
- 虽然是线程安全的，但因为它的底层实现是数组 + 链表的形式，所以在数据比较多的情况下访问是很慢的，因为要遍历整个链表，而 JDK 1.8 则使用了数组 + 链表/红黑树的方式优化了 ConcurrentHashMap 的实现，从之前的 O(n) 优化到了 O(logn) 的时间复杂度。

### 常见设计模式
1. 单例模式 (Singleton)
	1. 保证一个类只有一个实例
	2. 例子：数据库连接池、Spring的默认Bean
```
public class TikTok {
    private static TikTok instance;
    private TikTok() {}  // 私有构造
    
    public static TikTok getInstance() {
        if(instance == null) {
            instance = new TikTok();
        }
        return instance;
    }
}
```
1. 工厂模式 (Factory)
	1. 不暴露创建逻辑，通过工厂类生成对象
	2. 例子：JDBC的DriverManager
```
interface Car { void drive(); }
class Tesla implements Car { /*...*/ }
class BMW implements Car { /*...*/ }

public class CarFactory {
    public static Car getCar(String type) {
        if("Tesla".equals(type)) return new Tesla();
        else return new BMW();
    }
}
```

1. **单例** - 唯一存在的事物（太阳、国家主席）
2. **工厂** - 生产标准化产品（玩具工厂）
3. **适配器** - 转换接口（让不兼容的接口能一起工作，例子：Java中的InputStreamReader）
4. **装饰器** - 层层包装（动态添加功能，不改变原类，例子：Java IO流体系）
5. **观察者** - 消息通知（当对象状态变化时自动通知依赖它的对象，例子：Java中的EventListener）
6. **策略** - 多种解决方案（封装算法，使它们可以互相替换，例子：Java中的Comparator）

### Java 注解(Annotation)的作用
注解是一种元数据，用来为代码添加“说明”。它本身不会直接影响程序的逻辑执行，但可以被编译器、开发工具或框架读取并用于特定的处理。

比如最常见的 `@Override` 在编译时进行检查，确保重写了父类的方法，防止拼写错误或者签名不一致。

其次，注解也被用于框架中，比如JUnit：`@Test` 会告诉测试框架这个方法是一个测试用例（或者 `@Autowired` 可以让 Spring 自动进行依赖注入）。

`另外，注解还可以自定义，我们可以根据业务需求定义自己的注解，并结合反射机制在运行时动态处理这些信息，从而实现更灵活的逻辑控制，比如权限校验、日志记录等。`
`所以整体来说，注解的作用就是给代码添加“说明书”，让编译器、开发工具或框架更智能地处理程序逻辑，提高代码的可读性和可维护性。`

### Java的不可变类（Immutable Class）
一旦创建，它的对象状态就**不能被修改**的类。也就是说，所有字段在对象创建后都保持不变。
- 例子：`String` 类 -> `String a = "hello";`，每次修改其实是创建了一个新的字符串对象，原来的内容不会变。

**实现一个不可变类：**
1. **类要声明为 `final`**，防止被继承后修改行为。
2. **所有字段都要是 `private final`**，保证只在构造函数中赋值一次。
3. **没有 setter 方法**，防止外部修改字段值。
4. **如果字段是对象引用，要做 defensive copy（防御性拷贝）**，防止外部通过引用修改内部状态。
不可变类的优点：
- **设计简单**：因为状态不会变化，逻辑更容易维护。
- **线程安全**：多个线程访问同一个对象不会有竞争条件；
- **可缓存、可复用**：比如在哈希表中作为 key 很安全；
```java
// 这个 `Person` 类就是不可变的，一旦创建后 `name` 和 `age` 无法更改。
public final class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}
```

### 访问修饰符（Access Modifiers）
private: 同类 (只能在 **本类内部** 访问)
default: 同类+同包 (没有写修饰符，就属于默认权限，只能在 同一个包中 被访问)
protected: 同类+同包+子类 (不同包的**子类**)
public: 同类+同包+子类+其他包

### 基本类型（Primitive Type）和 包装类型（Wrapper Class）
Java 中有 8 种基本类型：`byte`、`short`、`int`、`long`、`float`、`double`、`char`、`boolean`
- 这些类型是 **存储在栈内存中的值类型**，性能高，占内存少。
Java 为每个基本类型提供了一个对应的 **包装类**，这些类都位于 `java.lang` 包中：
    - `int` → `Integer`，`boolean` → `Boolean` ……以此类推
- 包装类是 **对象类型（引用类型）**，存储在堆内存中，可以用于集合等只支持对象的场景。
从 Java 5 开始，Java 支持自动转换：
- **装箱（boxing）：基本类型 → 包装类型**
- **拆箱（unboxing）：包装类型 → 基本类型**
```
Integer x = 10;   // 自动装箱：int → Integer
int y = x + 5;    // 自动拆箱：Integer → int
```

### Exception 和 Error 的区别
`Exception` 和 `Error` 都是从 `Throwable` 类继承下来的，用来表示程序运行中发生的问题。

**Exception（异常）：**
程序**可以捕获和处理**的问题，又可以分为两类：
1. **Checked Exception（受检异常）**
    - 用 `try-catch` 处理，或者在方法上用 `throws` 抛出。
    - 比如：`IOException`、`SQLException`、`FileNotFoundException`
    - 适用于**程序外部的问题**，比如文件、网络、数据库等操作失败。
        
2. **Unchecked Exception（非受检异常）**
    - 编译时不强制处理，运行时可能会抛出。
    - 是 `RuntimeException` 的子类，比如：`NullPointerException`、`IndexOutOfBoundsException`、`IllegalArgumentException`
    - 多数是**程序逻辑错误**导致的。
        
**Error（错误）：**
 **JVM 层面的问题**，通常是程序**无法恢复或处理的**，通常不处理，处理也没意义，应该让程序崩溃。
- 常见`Error` ：`OutOfMemoryError` (内存溢出), `StackOverflowError` (栈溢出), `NoClassDefFoundError` (类加载失败)
- 这些错误大多数表示 JVM 本身出了问题，不是业务代码可以解决的。

### 方法重载（Overloading）和方法重写（Overriding）
**方法重载**: 编译时多态，让方法有多个版本
- **在同一个类中**，**方法名相同，但参数列表不同**（参数个数、类型不同，顺序不同也可以）。
- 发生在 **同一个类** 中
- **返回值可以不同**，但不能仅靠返回值区分
- 常用于构造函数或提供多种调用方式
```
public class Calculator {
	// 这里的 `add` 方法就是重载了，参数不一样，调用时编译器会自动根据参数类型来选择合适的方法。
    public int add(int a, int b) { return a + b; }

    public double add(double a, double b) { return a + b; }

    public int add(int a, int b, int c) { return a + b + c; }
}
```

**方法重写**: 运行时多态，让子类可以定制父类的方法行为。
- **子类继承父类时**，对子类中继承过来的方法进行**重新定义**。
- 发生在 **父类和子类之间**
- **方法名、参数列表完全一致**
- 返回值类型必须兼容（Java 5 之后允许协变返回）
- 访问修饰符不能比父类更严格
- 需要用 `@Override` 注解标记（不是必须，但强烈推荐）
```
class Animal {
    public void speak() { System.out.println("Huzzh"); }
}

class Cat extends Animal {
	// 重写了 `Animal` 的 `speak()` 方法，实现了多态。
    @Override
    public void speak() { System.out.println("Meow"); }
}
```

### Interface（接口）和 Abstract Class（抽象类）
**`interface` 是接口**，适合用来定义规范或功能，强调的是：**我能做什么**。
- 沒有构造函数
- 一个类可以实现多个接口
- 修饰符：方法默认 `public abstract`，变量是 `public static final`
**`abstract class` 是抽象类**，适合用来表示一类实体的共性，强调的是：**我是什么**。
- 可以有构造函数和完整方法实现
- 一个类只能继承一个抽象类
```
interface Flyable {
    void fly();  // 抽象方法
}

abstract class Animal {
    String name;

    Animal(String name) { this.name = name; }

    abstract void speak();  // 抽象方法

    void sleep() { System.out.println("正在睡觉"); }
}
```

### 泛型（Generics）
为什么需要泛型？
1. **类型不安全**：可能加入错误类型对象，编译器不会报错
2. **需要强制类型转换**，容易抛出 `ClassCastException`
有了泛型后的好处：
3. **类型安全**：编译阶段就能检查出类型错误，避免了在运行时出现类型转换异常，避免了在运行时出现类型转换异常。
4. **省去了强制类型转换**
5. **代码更清晰，更易维护**
6. **提高代码复用性**
```
//Case: 沒有泛型
List list = new ArrayList();
list.add("hello");
list.add(123);  // 不报错

String str = (String) list.get(0);  // 要强转
---------------
//Case: 有泛型
List<String> list = new ArrayList<>();
list.add("hello");
// list.add(123);  // 编译期报错！

String str = list.get(0);  // 不用强转
```

### hashCode() 和 equals()和==
== 比较的是两个引用**是否指向同一个对象地址（内存地址）**。
- 比如，System.out.println(new String("tt") == new String("tt")); // false，因为是两个不同的对象

equals()方法：
- 用来比较两个对象的“**内容是否相等**”
- 默认情况下，`Object` 类中的 `equals()` 是比较对象的地址（）
- 通常我们需要 **重写** `equals()` 方法，定义什么情况下两个对象被认为是“相等的”

hashCode()方法：
- 返回一个整数值，用来表示对象的**哈希值**
- 主要用于 **哈希结构中确定对象的存储位置**，比如 `HashMap`、`HashSet`
- 默认情况下，`Object` 中的 `hashCode()` 也是根据内存地址计算的
- **如果两个对象通过 `equals()` 判断相等，则它们的 `hashCode()` 必须相同**。但反过来不一定。
	- 如果你重写了 `equals()`，也应该同时重写 `hashCode()`。
	- 如果你只重写了 `equals()` 而没重写 `hashCode()`，在使用 `HashSet` 或 `HashMap` 时就会出现**“相等对象存进了不同的位置”**的问题。
```
// equals() Example
@Override
public boolean equals(Object obj) {
    if (this == obj) return true;
    if (obj == null || getClass() != obj.getClass()) return false;
    Person person = (Person) obj;
    return age == person.age && name.equals(person.name);
}

// hashCode() Example
Set<Person> set = new HashSet<>();
Person p1 = new Person("小明", 20);
Person p2 = new Person("小明", 20);
set.add(p1);
set.add(p2);  // 如果没重写 hashCode，会被认为是两个不同对象！
```

### 深拷贝和浅拷贝的区别
**浅拷贝（Shallow Copy）**
- **只复制对象本身，里面的引用对象不会复制**
- 拷贝后的对象与原对象内部仍然**共享同一个引用对象**
**深拷贝（Deep Copy）**
- **不仅复制对象本身，还复制它引用的所有子对象**
- 原对象和拷贝对象之间完全独立，互不影响
实现方式有：
1. 手动重写 `clone()` 方法，对每个字段递归 clone
2. 使用序列化与反序列化（如 `ObjectOutputStream`）
3. 使用第三方库（如 Apache Commons Lang 的 `SerializationUtils`）
```
class Person {
    String name;
    Address address;
}

Person p1 = new Person();
p1.name = "Alice";
p1.address = new Address("NY");

// 浅拷贝
Person p2 = p1;
// 此时：`p1.address == p2.address`，修改 `p2.address.city` 会影响 `p1`
```

### volatile 关键字
TBC (still not clear)
它的作用是确保 **多线程环境中变量的可见性**，并防止 **指令重排序**。
- **保证可见性**：
    - 当一个线程修改了 `volatile` 变量的值，其他线程能立即看到这个修改，避免了缓存数据的问题。
    - 在多线程环境中，JVM 会把 `volatile` 变量的值直接从主内存读取，而不是从线程的本地缓存中读取。
- **防止指令重排序**：
    - `volatile` 还能够禁止 JVM 对该变量进行 **指令重排序优化**，保证代码的执行顺序符合预期。
    **注意：** `volatile` 只能保证单一的 **变量操作**（读/写）具有原子性，但 **复合操作**（如 `i++`）不能保证原子性。
**限制**
1. **只保证可见性，不保证原子性**：
    - `volatile` 只能保证 **单一操作**（如读取和写入）的原子性，但无法保证复合操作（例如 `i++`）的原子性。
2. **不能用于替代锁**：
    - 如果要操作复合操作，仍然需要使用 **同步（synchronized）** 或 **原子变量**。
```
public class Example {
	// 适用于 **状态标志**（例如在多线程中表示某个线程是否继续运行）
    private volatile boolean flag = false;

    public void toggleFlag() { flag = !flag; }

    public boolean checkFlag() { return flag; }
}
```

### 类的加载过程
加载 → 连接（验证、准备、解析）→ 初始化 → 使用 → 卸载
一、加载（Load）
- JVM 通过类的 **全限定名**（即包名+类名）查找 `.class` 文件
- 读取字节码内容，生成对应的 `Class` 对象
- 这个阶段还确定使用哪个 **类加载器（ClassLoader）**
二、连接（Link）
连接过程又分为三个小阶段：
1. **验证（Verify）**：校验 `.class` 文件是否合法，比如字节码是否被篡改
2. **准备（Prepare）**：为静态变量分配内存，并设置默认值（不是赋初始值）
3. **解析（Resolve）**：将类、接口、字段、方法等的符号引用转换为直接引用
三、初始化（Initialize）
- 真正执行类中的 **静态初始化代码（静态代码块）和静态变量赋值**
- 这是类加载的最后一步，**只有到了这一阶段，类才真正“初始化完毕”**
四、使用（Use）
- 类已经加载好了，JVM 就可以创建对象、调用静态方法、访问字段等
- 这是我们代码运行的阶段
五、卸载（Unload）
- 类不再被使用时，JVM 会将类卸载出内存（这个过程不常发生）
- 卸载由垃圾回收器自动完成，开发者无法手动控制

### 内部类（Inner Class）
定义在 **另一个类内部的类**，可以更好地组织代码、封装逻辑。
- 成员内部类: 可以访问外部类的所有成员（包括 private）
```
public class Outer {
    private String name = "外部类";

    class Inner {
        void sayHello() { System.out.println("Hello from " + name); }
    }
}
// 调用方式：
Outer outer = new Outer();
Outer.Inner inner = outer.new Inner();
inner.sayHello();
```
- 局部内部类: 只能在当前方法中使用
```
public void doSomething() {
    class LocalInner {
        void print() {
            System.out.println("局部内部类");
        }
    }
    LocalInner local = new LocalInner();
    local.print();
}
```
- 匿名内部类: 常用于简化接口或抽象类的实现（常用于回调）
```
Runnable r = new Runnable() {
    public void run() {
        System.out.println("匿名内部类实现线程");
    }
};
new Thread(r).start();
```
- 静态内部类: 类似外部类，不可以访问外部类的非静态成员
```
public class Outer {
    static class StaticInner {
        void show() { System.out.println("我是静态内部类"); }
    }
}
// 调用方式：
Outer.StaticInner inner = new Outer.StaticInner();
inner.show();
```

### 栈（Stack）和队列（Queue）
栈是后进先出，适合处理临时数据结构；队列是先进先出，适合调度与资源管理，两者在 Java 中有不同的类支持和应用场景。

### 动态代理（Dynamic Proxy）
TBC (still not clear)
代理就是：通过一个中间对象（代理对象）来间接调用目标对象的方法。
Java 中有两种代理方式：
- **静态代理**：代理类是提前写好的
- **动态代理**：代理类是**在运行时动态生成**的（在运行时创建代理对象的机制，常用于在不改动源码的情况下，对方法进行增强）

Java 提供了两种主流的动态代理实现方式：
1. **JDK 动态代理**（基于接口）
	- 使用 Java 提供的 `java.lang.reflect.Proxy` 和 `InvocationHandler`
	- 要求目标类必须实现一个或多个接口
2. **CGLIB 动态代理**（基于继承）
	- 使用第三方库 CGLIB（Spring AOP 就是用它）
	- 通过**继承目标类并重写方法**来实现代理
	- 适用于没有接口的类
3. 应用场景：日志记录, 权限控制, 缓存处理
```
public interface UserService {
    void login(String username);
}

public class UserServiceImpl implements UserService {
    public void login(String username) {
        System.out.println(username + " 登录成功");
    }
}
------------------------
import java.lang.reflect.*;

public class ProxyFactory {
    public static Object getProxy(Object target) {
        return Proxy.newProxyInstance(
            target.getClass().getClassLoader(),
            target.getClass().getInterfaces(),
            new InvocationHandler() {
                public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                    System.out.println("开始执行方法：" + method.getName());
                    Object result = method.invoke(target, args);
                    System.out.println("方法执行完毕");
                    return result;
                }
            }
        );
    }
}

----------------------
// Use Case
UserService service = (UserService) ProxyFactory.getProxy(new UserServiceImpl());
service.login("张三");
```

### SPI（Service Provider Interface）机制
TBC (still not clear)
它允许框架（或模块）在 **运行时动态加载第三方实现类**，实现了 **模块解耦** 和 **插件化开发**。
```
// 1. 定义服务接口
public interface MyService {
    void execute();
}
// 2. 创建实现类
public class MyServiceImplA implements MyService {
    public void execute() {
        System.out.println("A 执行");
    }
}
// 3. 配置 SPI 描述文件：
// 3.1 在资源目录下添加文件：
META-INF/services/com.example.MyService
// 3.2 文件内容写上实现类的全限定类名：
com.example.MyServiceImplA
com.example.MyServiceImplB
// 4. 加载服务
ServiceLoader<MyService> loader = ServiceLoader.load(MyService.class);
for (MyService service : loader) {
    service.execute();
}
```
### Java反射（Reflection）
TBC (still not fully clear)
反射可以让程序在运行时查看和操作类、方法、字段等内部信息。

### Java线程安全
线程安全: 当多个线程同时操作共享数据时，保证数据始终正确

常见线程安全问题
1. 竞态条件（Race Condition）→ 两个线程同时执行`count++`，可能少加一次
2. 内存可见性问题 → 一个线程改了数据，其他线程看不见

线程安全解决方案
1. 加锁（synchronized）
	1. 当一个线程进入同步区域（加锁区域）时，会自动获得锁
	2. 其他线程必须等待当前线程完成操作并释放锁
	3. 确保同一时间只有一个线程能操作关键数据
		1. 方法级锁：整个方法加锁
		2. 代码块锁：`synchronized(obj) { ... }`
	4. 适用场景：
		1. 对共享数据进行复杂操作（如转账：先查余额再扣款）
		2. 需要保证一系列操作不可分割（原子性）
2. volatile关键字
	1. 当线程修改volatile变量时，新值会立即写入主内存
	2. 其他线程读取时，会强制从主内存重新加载最新值
	3. 保证所有线程看到的都是最新值
	4. **保证可见性（但不保证原子性）**
	5. 适用场景：简单的状态标志位（如开关控制 / isRunning）
3. 原子类（AtomicInteger等）
	1. 线程操作时会记录当前值的"期望值"
	2. 提交修改时检查值是否被其他线程改过
	3. 如果没被改过就更新，否则重试（自旋）
	4. 原理：CAS（Compare-And-Swap）无锁技术
	5. 适用场景：计数器场景（如网站访问量统计）
4. 线程安全集合 
	1. 专门为多线程设计的容器
	2. 根据不同集合采用不同策略：
		1. **分段锁**：将数据分成多个区块，只锁住操作的部分（如ConcurrentHashMap）
		2. **写时复制**：修改时创建新副本，不影响读操作（如CopyOnWriteArrayList）
		3. **完全同步**：所有方法都加锁（如Collections.synchronizedList包装的集合）
	3. 适用场景：共享数据容器（如缓存系统）
5. ThreadLocal 
	1. 每个线程有自己的独立副本
	2. 每个线程首次访问时自动初始化值
	3. 每个线程只能看到和修改自己的副本
	4. 线程结束时自动清理资源
	5. 适用场景：用户会话信息（如当前登录用户），SimpleDateFormat（避免创建大量对象）

### Java集合中哪些线程安全和不安全
不安全集合（需要自己加锁）：`ArrayList`, `HashMap`, `HashSet`, `LinkedList`
安全集合：`Vector` (老古董，不推荐), `Hashtable` (老古董，不推荐), `ConcurrentHashMap` (推荐), `CopyOnWriteArrayList` (读多写少场景推荐), `Collections.synchronizedList()` (包装器方法)

### wait() 和 sleep()
wait() 用于线程通信并且会释放锁，而 sleep() 是让线程暂停一段时间但不释放锁。
- wait() 一般配合 notify() 使用，常用于生产者-消费者模型中的线程通信。
- sleep() 是一个静态方法，常用于模拟延时或调度控制。
```
synchronized(obj) {
    obj.wait();  // 当前线程进入等待状态，并释放 obj 的锁
}
--------
Thread.sleep(1000); // 当前线程睡眠 1 秒，不释放任何锁
```

### 悲观锁和乐观锁的区别
悲观锁的思想是：**假设总是会发生并发冲突**，所以在访问数据前就上锁，**其他线程不能同时访问这份数据**。
- 常见实现方式有：`synchronized`, `ReentrantLock`, 数据库的 `select ... for update`
乐观锁的思想是：**假设并发冲突很少发生**，所以在读数据时不加锁，**在写入时检查是否有冲突**，如果有冲突再重试。
- 常见实现方式是 **CAS（Compare And Swap）比较并交换**。
- Java 中常用的类有：
    - `AtomicInteger`、`AtomicReference`（`java.util.concurrent.atomic` 包）
    - 数据库中的乐观锁通常用 **版本号（version）机制** 或时间戳。

## SpringBoot
### SpringBoot常见注解

| `@SpringBootApplication` | 启动类必备     |
| ------------------------ | --------- |
| `@RestController`        | 声明REST控制器 |
| `@Autowired`             | 自动注入依赖    |
| `@Service`               | 业务逻辑层     |
| `@Repository`            | 数据访问层     |
| `@Component`             | 通用组件      |
| `@Configuration`         | 配置类       |
| `@Bean`                  | 声明一个Bean  |
| `@Value`                 | 注入配置值     |
| `@RequestMapping`        | 映射URL路径   |
####  @Autowired 和 @Resource 注解
TBC (still not fully clear)
都是用来实现依赖注入的注解，区别如下：
- **来源**:`@Autowired` 是Spring框架提供的注解。`@Resource` 是Java本身提供。
- **依赖性**：使用`@Autowired` 时，通常需要依赖Spring的框架。使用`@Resource` 时，即使不在Spring框架下，也可以在任何符合Java EE规范的环境中工作。
- **使用场景**：当你需要更细粒度的控制注入过程，或者你需要支持Spring框架之外的Java EE环境时，`@Resource` 注解可能是一个更好的选择；如果你完全在Spring的环境下工作，并且希望通过类型自动装配，`@Autowired` 是更常见的选择。
- **属性**:`@Autowired` 可以不指定任何属性，仅通过类型自动装配。`@Resource` 可以指定一个名为`name`的属性，该属性表示要注入的bean的名称。
- **注入方式**：`@Autowired` 默认是通过类型（byType）进行注入。如果容器中存在多个相同类型的实例，它还可以与`@Qualifier`注解一起使用，通过指定bean的id来注入特定的实例。`@Resource` 默认是通过名称（byName）进行注入。如果未指定名称，则会尝试通过类型进行匹配。

✔ **用@Autowired当**：
- 项目纯Spring环境
- 喜欢简洁的按类型自动装配
- 需要和其他Spring特性（如@Primary）配合使用

✔ **用@Resource当**：
- 需要兼容非Spring环境
- 想要更精确地按名称注入
- 项目已经有Java EE的依赖

### Bean是线程安全的吗 
**无状态Bean**（没有成员变量或只有final变量）：安全
**有状态Bean**（有可修改的成员变量）：不安全
**如何保证安全**：
1. 尽量设计无状态Bean
2. 使用`synchronized`加锁
3. 使用`ThreadLocal`变量
4. 使用并发容器（如`AtomicInteger`）

### 依赖倒置 / 控制反转 / 依赖注入
**依赖倒置**：高层模块不依赖低层模块，它们共同依赖同一个抽象。抽象不要依赖具体实现细节，具体实现细节依赖抽象。

**控制反转**：“控制”指的是对程序执行流程的控制，而“反转”指的是在没有使用框架之前，程序员自己控制整个程序的执行。*在使用框架之后*，整个程序的执行流程通过框架来控制。流程的控制权从程序员“反转”给了框架。

**依赖注入**
不通过 new 的方式在类内部创建依赖类的对象，而是将依赖的类对象在外部创建好之后，通过构造函数、函数参数等方式传递（或注入）给类来使用。
- 不用自己管理对象创建
- 方便替换实现（如测试时可以用Mock对象）
- 降低耦合度
```
**传统方式（自己做饭）**
public class Restaurant {
    private Chef chef = new Chef(); // 自己雇厨师
    private Waiter waiter = new Waiter(); // 自己雇服务员
}
1. **依赖注入 - 字段注入（点外卖）**
public class Restaurant {
    @Autowired  // 告诉Spring："我要一个厨师"
    private Chef chef;
    
    @Autowired  // "我还要一个服务员"
    private Waiter waiter;
}
2. **依赖注入 - 构造器注入：通过构造函数传递依赖对象，保证对象初始化时依赖已就绪。**
@Service
public class OrderService {
    private final PaymentService paymentService;
    
    @Autowired // Spring 4.3+可以省略
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
3. **依赖注入 - Setter 方法注入：通过Setter方法设置依赖，灵活性高，但依赖可能未完全初始化。**
```

## Database
### AVL VS B+ VS Red-Black Tree
#### AVL Tree（平衡二叉搜索树）
**特点**：    
- 每次插入/删除都会检查平衡
- 左右子树高度差不超过1
- 旋转操作多（左旋/右旋）    
**优点**：查询快（O(log n)），绝对平衡
**缺点**：维护平衡代价高
**用途**：适合查询多、修改少的场景，如内存数据库索引
#### B+ Tree（多路平衡搜索树）
**特点**：    
- 一个节点可以有多个子节点（不像二叉树只有2个）
- 数据只存在叶子节点
- 叶子节点用指针连接    
**优点**：
- 高度低，磁盘IO少（适合数据库）
- 范围查询高效（叶子节点链表） 
**缺点**：结构较复杂
**用途**：数据库索引（MySQL的InnoDB引擎）
#### 红黑树（自平衡二叉搜索树）
**特点**：
- 通过"红黑规则"保持大致平衡
- 不像AVL树那么严格平衡
- 插入/删除旋转操作较少
**优点**：插入删除比AVL树快，仍保持较好查询性能
**缺点**：查询稍慢于AVL树
**用途**：Java的TreeMap、C++的STL map
规则：
> 1. 节点是红或黑
> 2. 根和叶子(NIL)是黑     
> 3. 红节点的子节点必须黑
> 4. 从任一节点到叶子的路径包含相同数量的黑节点

### SQL VS NoSQL
**SQL**关系型数据库 - 主要代表：SQL Server，MySQL(开源)，PostgreSQL(开源)，Oracle。
- 存储结构化数据。这些数据逻辑上
- 以表的形式存在，每一列代表数据的一种属性，每一行代表一个数据实体。

**NoSQL**非关系型数据库 - 主要代表：MongoDB，Redis。
- 文档型：MongoDB（类似JSON文件柜）
- 键值型：Redis（像字典/电话簿）
- 列存储：Cassandra（像竖着放的Excel）
- 图数据库：Neo4j（像人际关系网）
适合
- 数据结构多变或不确定
- 需要处理海量数据和高并发
- 需要快速迭代开发
- 数据可以容忍暂时不一致

**选择** SQL vs NoSQL，考虑以下因素。
- ACID vs BASE
	- 关系型数据库支持 ACID 即原子性，一致性，隔离性和持续性。
	- NoSQL 采用更宽松的模型 BASE ， 即基本可用，软状态和最终一致性。
		- 需要考虑对于面对的应用场景，ACID 是否是必须的。
			- 银行应用就必须保证 ACID，否则一笔钱可能被使用两次
			- 社交软件不必保证 ACID，因为一条状态的更新对于所有用户读取先后时间有数秒不同并不影响使用
		- 需要保证 ACID 的应用，我们可以优先考虑 SQL。反之则可以优先考虑 NoSQL。
- 扩展性对比
	- NoSQL数据之间无关系，这样就非常容易扩展。
		- 比如Redis自带主从复制模式、哨兵模式、切片集群模式。
		- 关系型数据库的数据之间存在关联性，水平扩展较难，需要解决跨服务器 JOIN，分布式事务等问题。
- 混合使用：很多系统同时使用两种数据库（如用MySQL存用户信息，用Redis缓存数据）

### MySQL
#### 事务 (ACID)
事务: 保证一组操作要么全部成功，要么全部失败回滚，绝不允许寄丢一半。
四大特性（ACID）
- 原子性（Atomicity）：
	- 一个事务中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。
	- 事务在执行过程中发生错误，会被回滚到事务开始前的状态，就像这个事务从来没有执行过一样。 
	- MySQL通过 undo log 来保证原子性的。
		- undo log 是一种用于撤销回退的日志。在事务没提交之前，MySQL 会先记录更新前的数据到 undo log 日志文件里面，当事务回滚时，可以利用 undo log 来进行回滚。
- 一致性（Consistency）：
	- 事务执行前后，数据必须满足预设的规则。
	- 比如，转账前后，钱要对得上账。  
- 隔离性（Isolation）：
	- 数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。
	- 多个事务同时使用相同的数据时，互不干扰，每个事务都有一个完整的数据空间，对其他并发事务是隔离的。
- 持久性（Durability）：
	- 事务处理结束后，操作结果永久保存，即便系统故障也不会丢失。  

#### 索引
专门的数据结构，帮助数据库快速找到记录。
```
**常见类型**
1. 普通索引（基础目录卡）
	1. 最基本的索引类型
	2. 相当于按书名首字母排序的卡片
	3. 允许重复值和NULL值
2. 唯一索引（防重目录卡）
	1. 类似普通索引，但不允许重复值
	2. 相当于"每本书必须有唯一ISBN号"的规则
	3. 主键索引就是一种特殊的唯一索引
3. 复合索引（组合目录卡）
	1. 同时按多个条件排序（如：先按作者姓，再按书名）
	2. 相当于图书馆的"作者+出版年份"联合检索卡
4. 全文索引（关键词检索卡）
	1. 专门用于文本内容的搜索
	2. 相当于书末的"关键词索引"页
	3. 适合WHERE MATCH...AGAINST查询
```
**工作原理: B+树结构（最常用）**
See [[#B+ Tree（多路平衡搜索树）]]：
- **根节点**：书的目录（指向各章节）
- **中间节点**：章节的子目录（指向具体页）
- **叶子节点**：真正的书页内容（包含所有数据或指针）
特点：
- 从根到叶子经过的节点数相同（平衡树）
- 叶子节点用指针连接，方便范围查询
##### 什么时候需要 / 不需要创建索引
优点（为什么用）
1. **查询加速**：百万数据中找1条记录，从分钟级→毫秒级
2. **排序优化**：ORDER BY不用临时排序
3. **连接加速**：JOIN操作效率提升
4. 该给哪些字段加索引: 
	1. **字段有唯一性限制**：如用户手机号、商品编码（重复值少的字段）
	2. **常用查询条件**：WHERE、JOIN、ORDER BY涉及的字段，这样能够提高整个表的查询速度
	3. 避免：性别、状态等低差异性字段

缺点（什么时候不用）
1. **占用空间**：索引就像多写了一本目录册，数量越大，占用空间越大
2. **降低写入速度**：每次增删改都要更新索引（像修改书要重编目录） 
3. **维护成本**：创建索引和维护索引要耗费时间，这种时间随着数据量的增加而增大，索引不是越多越好，需要合理设计

##### 索引失效的常见情况
- 使用函数：`WHERE YEAR(create_time) = 2023`（改成范围查询）
- 模糊查询：`LIKE '%关键字%'`（前导通配符导致失效）
- 类型转换：字符串字段用数字查询（`WHERE phone = 13800138000`应加引号）

#### Left Join / Right Join / Inner Join / 外连接
内连接 (INNER JOIN) : 结果只包含**两表都存在的**匹配记录
左连接 (LEFT JOIN) : **保留左表所有**记录，右表无匹配则填NULL
右连接 (RIGHT JOIN) : **保留右表所有**记录，左表无匹配则填NULL
全外连接 (FULL OUTER JOIN) ：**保留两表所有**记录，无匹配处填NULL
- MySQL不直接支持，但可用UNION实现
- 就像把左连接和右连接结果合并

**实际应用**：
- 要全部主表数据用左连
- 只要**匹配**数据用内连
- 偶尔用右连，全连很少见
```
-- 找出从未被订购的商品（用LEFT JOIN）
SELECT products.name
FROM products
LEFT JOIN orders ON products.id = orders.product_id
WHERE orders.product_id IS NULL;
```

#### 隔离级别
事务的隔离性: 解决"当多个操作同时发生时，数据会如何显示"的问题。

事务的隔离级别（从宽松到严格）
1. **读未提交 (read uncommitted)**
	1. 一个事务还没提交时，它做的变更就能被其他事务看到 (就像隔着玻璃门看别人数钱)
	2. 能看到别人正在数但还没存进去的钱
	3. 问题最多：可能看到脏读、不可重复读和幻读    
2. **读已提交 (read committed)**
	1. 一个事务提交之后，它做的变更才能被其他事务看到 (等别人把钱存进保险箱才让你看)
	2. 只能看到别人已经完成的操作
	3. 解决了脏读，但可能出现前后读取不一致 (不可重复读和幻读)
        
3. **可重复读 (repeatable read, MySQL InnoDB引擎默认)**
	1. 一个事务执行过程中看到的数据，一直跟这个事务启动时看到的数据是一致的
	2. 在整个事务中，你看到的数据就像开始时的照片一样不变
	3. 解决了脏读和不一致问题，但可能有"幻觉数据"（幻读, 新出现的记录）
        
4. **串行化 (serializable)** - 像银行VIP室，一次只服务一个人
	1. 会对记录加上读写锁，在多个事务对这条记录进行读写操作时，如果发生了读写冲突的时候，后访问的事务必须等前一个事务执行完成，才能继续执行
	2. 完全排队，一个接一个操作
	3. 最安全但最慢 (脏读、不可重复读和幻读现象都不可能会发生)

MySQL默认级别 - 可重复读隔离级别

#### 脏读 / 幻读
脏读（Dirty Read）— 看到别人的草稿
- **情况**：你排队时，看到前面客户正在填写的转账单（但他还没最终确认）
- **风险**：如果他最后改了金额或取消转账，你看到的信息就是错的
- **数据库表现**：事务A读取了事务B**未提交**的修改，如果B回滚，A读到的就是"脏数据"

幻读（Phantom Read）— 突然有人插队
- **情况**：你数了数前面有3个人，但当你准备办理时，突然又多出2个（期间有新客户取了号） 
- **风险**：你基于最初看到的人数做了错误判断
- **数据库表现**：事务A第一次查询有3条记录，第二次查询时由于其他事务插入了新数据，突然变成5条，像出现了"幻觉"

**如何解决幻读**
**尽量在开启事务之后，马上执行 select ... for update 这类锁定读的语句**，因为它会对记录加 next-key lock，从而避免其他事务插入一条新记录，就避免了幻读的问题。

### Redis
#### Redis底层的数据结构
Source: https://xiaolincoding.com/backend_interview/internet_giants/byte_dance.html#redis-%E6%9C%89%E5%93%AA%E4%BA%9B%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84
常见五种数据类型：
- String（字符串）：缓存对象、常规计数、分布式锁、共享session信息等。
- Hash（哈希）：缓存对象、购物车等。
- List（列表）：消息队列（但是有两个问题：1.生产者需要自行实现全局唯一ID；2.不能以消费组形式消费数据）等。
- Set（集合）：聚合计算（并集、交集、差集）场景，比如点赞、共同关注、抽奖活动等。
- Zset（有序集合）：排序场景，比如排行榜、电话和姓名排序等。
新增四种数据类型：
- BitMap（2.2版新增）：二值状态统计的场景，比如签到、判断用户登陆状态、连续签到用户总数等。
- HyperLogLog（2.8版新增）：海量数据基数统计的场景，比如百万级网页UV计数等。
- GEO（3.2版新增）：存储地理位置信息的场景，比如滴滴叫车。
- Stream（5.0版新增）：消息队列，相比于基于List类型实现的消息队列，有这两个特有的特性：自动生成全局唯一消息ID，支持以消费组形式消费数据。

#### Redis为什么这么快？
Source: https://xiaolincoding.com/backend_interview/internet_medium/xiaohongshu.html#redis%E4%B8%BA%E4%BB%80%E4%B9%88%E5%BF%AB

- Redis的大部分操作都在内存中完成，并且采用了高效的数据结构
	- 因此Redis瓶颈可能是机器的内存或者网络带宽，而并非 CPU
	- 既然CPU不是瓶颈，那么自然就采用单线程的解决方案了 
- 不受CPU限制，因此采用单线程模型
	- 避免多线程之间的竞争，省去了多线程切换带来的时间和性能上的开销，而且也不会导致死锁问题。  
		- 死锁问题: 
			- A线程：抢到了菜刀（锁1），但需要锅（锁2）才能继续。
			- B线程：抢到了锅（锁2），但需要菜刀（锁1）才能继续。
			- 结果：两人互相卡住，谁都做不了菜，这就是**死锁**。
		- Redis只用1个厨师（单线程），独享所有工具（资源），沒有竞争自然不会死锁。
- 采用**I/O多路复用机制**处理大量的客户端Socket请求
	- IO多路复用机制
		- 一个线程处理多个 IO 流 (select/epoll机制)
			- 在只运行单线程的情况下，该机制允许epoll同时监听多个Socket连接。
			- 一旦有请求到达，就会交给Redis线程处理，这就实现了一个Redis线程处理多个 IO 流的效果。  
- 单线程不会慢吗？
	- 不用排队等（无锁竞争），所有业务秒办（内存操作），一次处理多个客户需求（多路复用），实际比多个普通窗口更高效。

#### Redis和MySQL如何保证一致性
Source: https://xiaolincoding.com/backend_interview/internet_giants/byte_dance.html#redis-%E5%92%8C-mysql-%E5%A6%82%E4%BD%95%E4%BF%9D%E8%AF%81%E4%B8%80%E8%87%B4%E6%80%A7
先更新数据库 + 再删除缓存 + 过期时间
- 因为**缓存的写入通常要远远快于数据库的写入**，如果先删缓存，在数据库更新完成前，其他请求可能瞬间把旧数据重新读到缓存，导致更长时间的不一致。
- `先更新数据库 -> 再删缓存`的优势：
	- 即使有请求在更新数据库期间读取了旧值，也会因后续请求的删除操作而失效，从而强制下一次读取从数据库拉取新值，不一致时间窗口极短。
- 双重保险：缓存过期时间
	- 即使极端情况下出现不一致（如请求A在请求B删除缓存后仍写入旧值），通过给缓存设置过期时间（如30秒），到期后缓存自动失效，后续请求会从数据库读取最新值。

#### 基于Redis实现分布式锁
Source: https://javaguide.cn/distributed-system/distributed-lock-implementations.html#%E5%A6%82%E4%BD%95%E5%9F%BA%E4%BA%8E-redis-%E5%AE%9E%E7%8E%B0%E4%B8%80%E4%B8%AA%E6%9C%80%E7%AE%80%E6%98%93%E7%9A%84%E5%88%86%E5%B8%83%E5%BC%8F%E9%94%81
Official Documentation: https://redis.io/docs/latest/develop/use/patterns/distributed-locks/
##### 分布式锁 (Distributed Lock)
在分布式环境下(多台机器或多个服务)，同一时间只有一个客户端(可能是线程、进程或机器)能够访问某个共享资源或执行某个操作。
- 互斥访问共享资源
- 与单机环境下的锁(如Java中的synchronized或ReentrantLock)不同，分布式锁需要解决网络延迟、节点故障等分布式环境特有的问题。

##### 实现原理
1. 获取锁(加锁)
	1. 使用Redis的`SETNX`(SET if Not eXists)命令：`SETNX lockKey uniqueValue`
	2. 返回1：表示key不存在，设置成功，获取到了锁; 返回0：表示key已存在，获取锁失败
	3. 这里的`uniqueValue`(唯一值)通常可以使用UUID或客户端ID等，用于后续安全释放锁。
2. 释放锁(解锁)
	1. 为了防止误删其他客户端持有的锁，使用Lua脚本先检查value是否匹配再删除
	2. 使用Lua脚本可以保证"检查value"和"删除key"这两个操作的原子性。如果不使用Lua脚本，可能会出现：
		1. 客户端A检查value匹配
		2. 锁过期自动释放
		3. 客户端B获取了锁
		4. 客户端A执行DEL命令，误删了客户端B的锁
3. 这种方式实现分布式锁存在一些问题
	1. 比如应用程序遇到一些问题比如释放锁的逻辑突然挂掉，可能会导致锁无法被释放，进而造成共享资源无法再被其他线程/进程访问。

##### 为什么要给锁设置一个过期时间
防止锁无法释放
1. 避免死锁  
	1. 如果不设置过期时间，当客户端获取锁后崩溃或发生网络故障，没有正常释放锁时，这个锁将永远存在于Redis中，导致其他客户端永远无法获取锁，形成死锁。
2. 系统健壮性  
	1. 即使客户端崩溃，锁也会在过期后自动释放，确保系统能够从故障中恢复。
3. 锁的优雅续期: Redisson
	1. Redisson中的分布式锁自带自动续期机制: Watch Dog（看门狗）
	2. 客户端获取锁后，启动一个后台线程定期检查业务是否仍在执行
	3. 如果操作共享资源的线程还未执行完成的话，Watch Dog 会不断地延长锁的过期时间，进而保证锁不会因为超时而被释放。
	4. 当业务完成时停止续期并释放锁

#### 缓存雪崩、击穿、穿透
- 缓存雪崩 (Cache Avalanche)
	- 当大量缓存数据在同一时间过期（失效）或者Redis故障宕机时，如果此时有大量的用户请求，无法在Redis中处理，于是全部请求都直接访问数据库，导致数据库的压力骤增，严重的会造成数据库宕机，从而形成一系列连锁反应，造成整个系统崩溃。
	- 解决方案
		- 错开缓存数据过期时间（添加随机偏移）
			- 如果要给缓存数据设置过期时间，应避免将大量的数据设置成同一个过期时间。
			- 在设置时，给缓存数据的过期时间加上一个随机数，保证数据不会在同一时间过期。
		- 互斥锁Mutex
			- 当业务线程在处理用户请求时，如果发现访问的数据不在Redis里，就加个互斥锁，保证同一时间内只有一个请求来构建缓存（从数据库读取数据，再将数据更新到Redis里）。
			- 当缓存构建完成后，再释放锁。未能获取互斥锁的请求，要么等待锁释放后重新读取缓存，要么就返回空值或者默认值。
			- 实现互斥锁的时候，最好设置*超时时间*，不然第一个请求拿到了锁，然后这个请求发生了某种意外而一直阻塞，一直不释放锁，这时其他请求也一直拿不到锁，整个系统就会出现无响应的现象。
		- 后台更新缓存
			- 业务线程不再负责更新缓存，缓存也不设置有效期，而是让缓存“永久有效”，并将更新缓存的工作交由后台线程定时更新。
- 缓存击穿 (Cache Breakdown)
	- 如果缓存中的某个热点数据(hotspot keys)过期了，此时大量的请求访问了该热点数据，就无法从缓存中读取，直接访问数据库，数据库很容易就被高并发的请求冲垮。
	- 解决方案
		- 热点数据特殊处理（热点密钥不会过期/使用异步更新）
			- 在热点数据准备要过期前，提前通知后台线程更新缓存且重新设置过期时间。
			- 不给热点数据设置过期时间，由后台异步更新缓存。
		- 互斥锁Mutex (like above)
			- 保证同一时间只有一个业务线程更新缓存，未能获取互斥锁的请求，要么等待锁释放后重新读取缓存，要么就返回空值或者默认值。
- 缓存穿透 (Cache Penetration)
	- 用户访问的数据不在缓存也不在数据库中，导致请求在访问缓存时，发现缓存缺失，再去访问数据库时，发现数据库中也没有要访问的数据，没办法构建缓存数据，来服务后续的请求。那么当有大量这样的请求到来时，数据库的压力骤增。
	- 解决方案
		- 限制非法请求, 严格验证请求参数
			- 在 API 入口处判断请求参数是否合理，请求参数是否含有非法值、请求字段是否存在。
			- 如果判断出是恶意请求就直接返回错误，避免进一步访问缓存和数据库。
		- 缓存空值或默认值
			- 针对查询的数据，可以在缓存中设置一个空值或者默认值，这样后续请求就可以从缓存中读取到空值或者默认值，返回给应用，而不会继续查询数据库。
		- 布隆过滤器(Bloom filter)预先检查数据是否存在
			- 在写入数据库数据时，使用布隆过滤器做个标记。
			- 在用户请求到来时，业务线程确认缓存失效后，可以通过查询布隆过滤器快速判断数据是否存在。
				- 如果不存在，就不用查询数据库。
			- 即使发生了缓存穿透，大量请求只会查询Redis和布隆过滤器，而不会查询数据库，保证了数据库正常运行。
			- Redis自身也是支持布隆过滤器的。

#### 集群部署
将多台服务器(也称为节点)组合在一起，共同对外提供服务。
在传统的基于会话(Session)和Cookie的身份验证方式中：
1. 用户登录后，服务器会在**自己的内存**中保存用户的登录状态
2. 当同一个用户的下次请求被分配到另一台服务器时，那台服务器没有这个用户的会话信息
3. 结果就是用户需要重新登录，体验很差
解决方案之一是用Redis等共享存储来保存会话信息，但这增加了系统复杂性。

## 计算机网络
### OSI 七层模型
- 应用层 (Application Layer): 用户接口和应用程序（如HTTP、FTP、SMTP）
- 表示层 (Presentation Layer): 数据格式化, 加密, 压缩（如SSL/TLS、JPEG编码）
- 会话层 (Session Layer): 应用程序之间通信会话（如SSH、RPC）
- 传输层 (Transport Layer): 主机之间数据传输服务（如TCP、UDP协议）
- 网络层 (Network Layer): 路由, **IP寻址**（如IP协议、路由器）
- 数据链路层 (Data Link Layer): 点对点数据传输服务, 原始比特流（如MAC地址、交换机）
- 物理层 (Physical Layer): 硬件设备（如网线、光纤信号）
![[tcp.png]]

### TCP和UDP区别 (准确性vs速度)
- 连接：TCP传输数据前先要建立连接；UDP 是不需要连接，即刻传输数据。
- 服务对象：TCP 是一对一，即一条连接只有两个端点。UDP 支持一对一、一对多、多对多。
- 可靠性：TCP 是可靠交付数据的，数据可以无差错、不丢失、不重复、按序到达。UDP 是尽最大努力交付，不保证可靠交付数据。
	- 但基于 UDP 的 QUIC 协议 可以实现类似 TCP 的可靠性传输
- 拥塞控制、流量控制：TCP 有拥塞控制和流量控制机制，保证数据传输的安全性。UDP 则没有，即使网络非常拥堵了，也不会影响 UDP 的发送速率。
- 首部开销：TCP 首部长度较长，会有一定的开销，首部在没有使用「选项」字段时是 20 个字节。UDP 首部只有 8 个字节，并且是固定不变的，开销较小。
- 传输方式：TCP 是流式传输，没有边界，但保证顺序和可靠。UDP 是一个包一个包的发送，是有边界的，但可能会丢包和乱序。
- TCP适用网页、邮件、文件传输，UDP适用视频会议、在线游戏、直播。

### TCP/IP 四层模型
TBC (to be clear further)
Source: https://javaguide.cn/cs-basics/network/tcp-connection-and-disconnection.html
### TCP 三次握手
1. **第一次握手（SYN=1, seq=x）**
    - 客户端发送"同步序列号"请求
    - 就像举手说："我要开始连接了！"
        
2. **第二次握手（SYN=1, ACK=1, seq=y, ack=x+1）**
    - 服务端确认收到请求，并发送自己的同步请求
    - 相当于回应："收到你的请求了，我也准备好了！"
        
3. **第三次握手（ACK=1, seq=x+1, ack=y+1）**
    - 客户端确认服务端的准备
    - 最后确认："好的，我们开始通信吧！"
        
**为什么要三次握手**
- **防止历史连接请求突然到达, 确认双方的收发能力正常**
- **第一次握手**：Client 什么都不能确认；Server 确认了对方发送正常，自己接收正常
- **第二次握手**：Client 确认了：自己发送、接收正常，对方发送、接收正常；Server 确认了：对方发送正常，自己接收正常
- **第三次握手**：Client 确认了：自己发送、接收正常，对方发送、接收正常；Server 确认了：自己发送、接收正常，对方发送、接收正常

**第2次握手传回了ack为什么还要传回syn**
服务端传回发送端所发送的 ACK 是为了告诉客户端：“我接收到的信息确实就是你所发送的信号了”，这表明从客户端到服务端的通信是正常的。回传 SYN 则是为了建立并确认从服务端到客户端的通信。

**三次握手过程中可以携带数据吗**
第三次握手是可以携带数据的(客户端发送完 ACK 确认包之后就进入 ESTABLISHED 状态了)
### TCP 四次挥手
1. **第一次挥手（FIN=1, seq=u）**
    - 主动关闭方（如客户端）发送终止请求
    - 表示："我的数据发完了"
2. **第二次挥手（ACK=1, ack=u+1）**
    - 被动关闭方（如服务端）确认收到终止请求
    - 回应："知道你不想发了，但我可能还有数据要发给你"
3. **第三次挥手（FIN=1, ACK=1, seq=v, ack=u+1）**
    - 被动关闭方发完剩余数据后，发送自己的终止请求
    - 表示："我也发完了，可以关了"
4. **第四次挥手（ACK=1, ack=v+1）**
    - 主动关闭方最后确认
    - 最终确认："好的，正式断开"

**为什么需要四次？**
- TCP是全双工的：两个方向的数据传输相互独立
- 必须分别关闭两个方向的数据流
- 中间可能有数据需要继续传输（第二次和第三次挥手之间的等待）

**为什么建立连接是三次，断开要四次？**  
A：建立连接时服务端的"SYN+ACK"可以合并发送，但断开时服务端收到FIN后可能还有数据要发送，所以ACK和FIN需要分开发送。

### 访问网页的全过程
- 从浏览器输入网址到网页显示，期间网络层面发生了什么？ 

1. 在浏览器中输入指定网页的 URL。
2. 浏览器通过 DNS 协议，获取域名对应的 IP 地址。
	1. 查浏览器缓存 → 翻自己的备忘录（最近查过的地址）     
	2. 查路由器缓存 → 问室友「你最近取过这个吗？」
	3. 查DNS服务器 → 打快递公司客服电话查仓库地址
	4. 结果：得到真实地址 `192.168.1.1`
3. 浏览器根据 IP 地址和端口号，向目标服务器发起一个 TCP 连接请求。
	1. 三次握手：
		1. 你打电话给仓库：「我要来取货啦！」（SYN）
		2. 仓库回复：「好的，我准备好了！」（SYN-ACK）
		3. 你确认：「那我出发了！」（ACK）
		4. 意义：确保双方都能正常通信，就像确认仓库有人值班才出发
4. 浏览器在 TCP 连接上，向服务器发送一个 HTTP 请求报文，请求获取网页的内容。
	1. 浏览器发送请求头（包含Cookies等信息）
	2. 用HTTP/HTTPS协议「说普通话」，而不是乱码
5. 服务器收到 HTTP 请求报文后，处理请求，并返回 HTTP 响应报文给浏览器。
	1. 验证身份（查Cookies）
	2. 从数据库调取网页数据
	3. 生成HTML响应（就像打包好你的包裹）
6. 浏览器收到 HTTP 响应报文后，解析响应体中的 HTML 代码，渲染网页的结构和样式，同时根据 HTML 中的其他资源的 URL（如图片、CSS、JS 等），再次发起 HTTP 请求，获取这些资源的内容，直到网页完全加载显示。
7. 浏览器不需要和服务器通信时，可以主动关闭 TCP 连接，或者等待服务器的关闭请求。
	1. 四次挥手：
		1. 你说：「货拿到了，我先走啦」（FIN）
		2. 仓库：「稍等，我确认下库存」（ACK）
		3. 仓库：「确认完了，拜拜」（FIN）
		4. 你：「好的，下次见」（ACK）

### 常见的状态码
1×× 提示信息，表示目前是协议处理中的**中间状态**，还需要后续的操作。
2×× **成功**，报文已经收到并被正确处理。
3×× 重定向，资源位置发生变动，需要客户端**重新发送**请求。
4×× 客户端错误，请求**报文有误**，服务器无法处理。
5×× 服务器错误，服务器在**处理请求**时内部发生了**错误**。  

### GET和POST和PUT的区别
Source: https://xiaolincoding.com/network/2_http/http_interview.html#get-%E4%B8%8E-post
- GET: 从服务器获取指定的资源
	- GET请求的参数位置一般是写在 **URL中**，URL 规定只能支持 **ASCII**，所以 GET 请求的参数只允许 ASCII 字符，且浏览器会对 URL 的长度有限制（HTTP协议本身对 URL长度并没有做任何规定）。
	- 可缓存
- POST: 根据请求负荷（报文body）对指定的资源做出处理
	- 请求携带数据的位置一般是写在报文 **body中**，body 中的数据可以是任意格式的数据，只要客户端与服务端协商好即可，且浏览器不会对 body 大小做限制。
	- 与PUT不同，对父资源执行操作，通常不缓存。
- PUT: 将请求体（body）中携带的表示（representation）**完整替换目标URI指定的资源**
	- 如果资源不存在，则根据是否允许创建返回201 (Created) 或 404 (Not Found)
	- 可缓存
- 安全: 请求方法不会'破坏'服务器上的资源
- 幂等: 多次执行相同的操作，结果相同
	- GET 方法是安全且幂等的，所以可以对 GET 请求的数据做**缓存**，这个缓存可以做到浏览器本身上（彻底避免浏览器发请求），也可以做到代理上（如nginx），而且在浏览器中 GET 请求可以保存为书签。
	- POST不安全且不幂等: '新增或提交数据'的操作，会修改服务器上的资源; 多次提交数据就会创建多个资源。浏览器一般不会缓存 POST 请求，也不能把 POST 请求保存为书签。
	- PUT不安全但幂等
- 如果「安全」放入概念是指信息是否会被泄漏的话，虽然 POST 用 body 传输数据，而 GET 用 URL 传输，这样数据会在浏览器地址拦容易看到，但是并*不能说 GET 不如 POST 安全*的。
	- 因为 HTTP 传输的内容都是明文的，虽然在浏览器地址拦看不到 POST 提交的 body 数据，只要抓个包就都能看到了。
	- 要避免传输过程中数据被窃取，使用 HTTPS 协议，这样所有 HTTP 的数据都会被加密传输。

### HTTP 与 HTTPS 协议的区别
- 安全
	- HTTP：明文传输数据，这使得它很容易被窃听和篡改。
	- HTTPS：使用SSL/TLS协议（SSL/TLS）对所有通信进行加密，确保数据的机密性和完整性。
- 建立连接
	- HTTP：只需要一个标准的TCP三次握手。
	- HTTPS：需要额外的SSL/TLS握手来建立安全加密。
- 默认端口
	- HTTP: port 80; HTTPS: port 443
- 身份验证Authentication
	- HTTP不进行身份验证; HTTPS：需要CA的数字证书来验证服务器的真实性。
- 性能
	- HTTP：更快的连接设置（没有加密开销）。
	- HTTPS：由于加密/解密过程稍慢，但提供关键的安全性。

### HTTP协议 VS RPC
#### RPC
RPC（Remote Procedure Call，远程过程调用）让程序能够像调用本地方法一样调用远程服务, 具体实现包括gRPC和Thrift。

HTTP的局限性
- 每次都要写完整的订单格式（HTTP报文头）
- 需要自己拆包装（数据序列化/反序列化）
- 数据格式: JSON/XML（文本）
- 短连接为主, 性能较低（HTTP/1.1的队头阻塞问题）
- 适用浏览器-服务器通信 or 需要人类可读的API（如公开API）
RPC的优势
- **透明性**：感觉像本地调用
- 数据格式: Protocol Buffers（二进制）
- 通常长连接, 性能高（二进制编码）
- 适用服务间内部通信（微服务通信）
#### gRPC
TBC (still not understand, relate to GO & distributed systems)
基于HTTP/2, RPC的实现
gRPC的局限性
- **浏览器支持有限**：需要grpc-web转换
- **调试不便**：二进制数据不易阅读
- **生态工具**：如Swagger不支持

### RESTful API
- 直观：URL告诉你资源是什么（名词）→ HTTP方法告诉你要做什么（动词）
- 统一：所有API都遵循相同规则
- 灵活：同样的`/books`地址，不同方法就有不同功能

### Token / Session / Cookie
**Token**
Token是包含**用户身份信息的加密字符串**，无状态，采用自包含设计，服务器不需要存储Token信息。
服务器收到token后解密就知道是哪个用户，需要开发者手动添加。

**工作流程**：
1. 用户登录 → 服务器验证凭证
2. 生成包含用户信息的Token（使用密钥签名）
3. 返回Token给客户端（通常通过JSON响应）
4. 客户端存储Token（localStorage或内存）
5. 后续请求在Authorization头中携带Token
6. 服务器验证签名并提取用户信息

**Session**
Session是**服务器**为每个用户创建**的临时存储空间**。服务器会给每个Session分配唯一ID，通过Cookie将这个ID传给浏览器。

**工作流程**：
1. 用户首次访问 → 服务器创建Session存储区（内存/数据库）
2. 生成唯一Session ID（如`a1b2c3d4`）
3. 通过Cookie将Session ID传给浏览器    
4. 浏览器后续请求自动携带这个ID
5. 服务器收到cookie后解析出Session ID，再去session列表中查找，找到相应session和依赖cookie。

**关键特点**：
- 实际用户数据（如购物车内容）存储在服务器端
- 默认依赖Cookie机制传递Session ID
- 会话结束时（浏览器关闭/超时）数据销毁

**Cookie**
Cookie是服务器发送到用户浏览器并**保存在本地**的一小块数据（最大4KB）。Cookie装有Session ID，存储在客户端，浏览器通常在后续请求中会自动添加。

**工作原理**：  
当用户首次访问网站时：
1. 服务器通过`Set-Cookie`响应头发送数据到浏览器
2. 浏览器保存这个Cookie
3. 之后对该网站的所有请求都会自动带上这个Cookie

**典型用途**：
- 记住登录状态（如"记住我"功能）
- 保存用户偏好（语言/主题设置）
- 跟踪用户行为（分析用户浏览路径）

#### 核心差异
1. 存储位置：Cookie (客户端 - 通常是浏览器), Session (服务器端)
2. 数据容量：
	1. 单个Cookie的大小限制通常在4KB左右，而且大多数浏览器对每个域名的总Cookie数量也有限制。
	2. 由于Session存储在服务器上，理论上不受数据大小的限制，主要受限于服务器的内存大小。
3. 安全性：
	1. Cookie相对不安全，因为数据存储在客户端，容易受到XSS（跨站脚本攻击）的威胁。
	2. Session通常认为比Cookie更安全，因为敏感数据存储在服务器端，但仍然需要防范Session劫持（通过获取他人的Session ID）和会话固定攻击。
4. 生命周期：
	1. Cookie可以设置过期时间，过期后自动删除。也可以设置为会话Cookie，即浏览器关闭时自动删除。
	2. Session在默认情况下，当用户关闭浏览器时，Session结束。但服务器也可以设置Session的超时时间，超过这个时间未活动，Session也会失效。
5. 性能：
	1. 因为Cookie随每个请求发送到服务器，在Cookie数据较大时可能会影响*网络传输效率*。
	2. 因为Session存储在服务器端，每次请求都需要查询服务器上的Session数据，这可能会增加*服务器的负载*，特别是在高并发场景下。

#### 如果客户端禁用了Cookie，Session还能用吗？
Session机制默认依赖Cookie传递Session ID，当浏览器禁用Cookie时，这个"信物"无法传递，导致服务器无法识别用户身份。

替代方案
1. URL重写：将Session ID附加到URL中作为参数，但分享链接可能导致Session ID的意外泄露。
2. 隐藏表单字段：在每个需要Session信息的HTML表单中包含一个隐藏字段，用来存储Session ID。
	1. 这种方法仅适用于通过表单提交的交互模式，不适合链接点击或Ajax请求。

#### 数据存储到LocalStorage VS Cookie
Cookie 适合用于在客户端和服务器之间传递数据、跨域访问和设置过期时间，而LocalStorage适合用于在同一域名下的不同页面之间共享数据、存储大量数据和永久存储数据。
1. 存储容量：
	1. Cookie 的存储容量通常较小（最大4KB），LocalStorage（MB）更适合存储大量数据
2. 数据发送：
	1. Cookie 在每次HTTP请求中都会自动发送到服务器，适用于在客户端和服务器之间传递数据。
	2. LocalStorage的数据不会自动发送到服务器，适合用于在同一域名下的不同页面之间共享数据。
3. 生命周期：
	1. Cookie 可以设置一个过期时间，使得数据在指定时间后自动过期。
	2. LocalStorage的数据将永久存储在浏览器中，除非通过 JavaScript 代码手动删除。
4. 安全性：
	1. Cookie的安全性较低，因为 Cookie 在每次 HTTP 请求中都会自动发送到服务器，存在被窃取或篡改的风险。
	2. LocalStorage的数据仅在浏览器端存储，不会自动发送到服务器，相对更安全。

### JWT(JSON Web Token)令牌
JWT就是一个**自包含的、经过数字签名的JSON数据包**，由三部分组成（用点号连接）：
1. 头部（Header）- 签名算法"alg" + 令牌类型"typ"
2. 载荷（Payload）
	1. **标准字段**（用户ID（subject）"sub" + 用户名 "name" + 签发时间（issued at） "iat"）
	2. **公共字段**：可自定义的公开信息
	3. **私有字段**：双方约定的敏感信息
3. 签名（Signature）- 把前两段用`.`连接，加上密钥（只有服务器知道），通过指定算法生成，最终形成第三段。

#### JWT令牌和传统方式的区别
1. 无状态性：JWT是无状态的令牌，不需要在服务器端存储会话信息。
	1. JWT令牌中包含了所有必要的信息，如用户身份、权限等。
	2. JWT在分布式系统中更加适用，可以方便地进行扩展和跨域访问。
2. 安全性：JWT使用密钥对令牌进行签名，确保令牌的完整性和真实性。
	1. 只有持有正确密钥的服务器才能对令牌进行验证和解析。
	2. 这种方式比传统的基于会话和Cookie的验证更加安全，有效防止了CSRF（跨站请求伪造）等攻击。
3. 跨域支持：JWT令牌可以在不同域之间传递
	1. 通过在请求的头部或参数中携带JWT令牌，可以实现无需Cookie的跨域身份验证。

#### JWT VS Session
TBC  (not understand yet)
JWT: 分布式/微服务, 多平台, 可接受短期风险, 高并发无状态验证
Session: 单体应用, 仅浏览器, 需要严格会话控制, 需要集中式会话管理

#### JWT的缺点
JWT 一旦派发出去，在失效之前都是有效的，无法**即时失效**。
解决方案
- 短期有效期（如accessToken 30分钟）
- 结合黑名单机制（Redis记录失效令牌）
	- 使用内存数据库比如Redis维护一个黑名单，想让某个JWT失效的话就直接将这个JWT加入到黑名单。每次使用JWT进行请求的话都会先判断这个JWT是否存在于黑名单中。

#### JWT令牌如果泄露了怎么解决
1. 及时失效令牌：当检测到JWT令牌泄露或存在风险时，可以立即将令牌标记为失效状态。
	1. 服务器在接收到带有失效标记的令牌时，会拒绝对其进行任何操作，从而保护用户的身份和数据安全。
2. 刷新令牌：当检测到令牌泄露时，可以主动刷新令牌，重新生成一个新的令牌，并将旧令牌标记为失效状态。
	1. 即使泄露的令牌被恶意使用，也会很快失效，减少了被攻击者滥用的风险。
3. 使用黑名单：服务器可以维护一个令牌的黑名单，将泄露的令牌添加到黑名单中。
	1. 在接收到令牌时，先检查令牌是否在黑名单中，如果在则拒绝操作。
	2. 这种方法需要服务器维护黑名单的状态，对性能有一定的影响，但可以有效地保护泄露的令牌不被滥用。

#### 前端如何存储JWT
存储位置
1. LocalStorage
	1. 优点：容量大(5MB)，不自动发送
	2. 缺点：易受XSS（跨站脚本攻击）攻击
	3. 适用：需要持久登录的SPA应用
2. SessionStorage
	1. 优点：标签页关闭自动清除
	2. 缺点：刷新页面需重新认证
	3. 适用：高安全要求的临时会话
3. HttpOnly Cookie
	1. 优点：防XSS（跨站脚本攻击），自动携带
	2. 缺点：有CSRF（跨站请求伪造）风险，4KB限制
	3. 适用：传统Web应用
4. 内存变量
	1. 1. 优点：最安全，页面刷新即丢失
	2. 缺点：体验差
	3. 适用：金融级安全应用

#### JWT令牌解决集群部署
##### 集群部署
将多台服务器(也称为节点)组合在一起，共同对外提供服务。

在传统的基于会话(Session)和Cookie的身份验证方式中：
1. 用户登录后，服务器会在**自己的内存**中保存用户的登录状态
2. 当同一个用户的下次请求被分配到另一台服务器时，那台服务器没有这个用户的会话信息
3. 结果就是用户需要重新登录，体验很差
解决方案之一是用Redis等共享存储来保存会话信息，但这增加了系统复杂性。

JWT(JSON Web Token)使集群中的每台服务器都能独立验证用户身份：
1. JWT令牌本身就包含了用户的身份信息，不需要服务器存储
2. 集群中的任何服务器收到JWT后，都可以自己验证其真实性
3. 不再需要Redis等共享会话存储，简化了架构

### WebSocket
TBC (to be clear)
WebSocket是一种"长连接"技术：
- 普通HTTP：每次都要发起请求, 挂断后必须重新发起请求才能再沟通
	- 单向（只能客户端发起）
	- 每次携带完整头部（较重）
- WebSocket：首次建立连接（相当于"频道调谐"）, 之后双方随时可以说话, **不用反复建立连接**
	- 双向（服务器可主动推送）
	- 首次握手后头部很小（轻量）
常见应用: 实时游戏, 聊天软件, 弹幕系统, 协同编辑, 股票实时行情

### 进程与线程
进程（Process）- 独立的工厂
- 有独立的厂房（内存空间），自己的生产线（程序代码），专用仓库（资源分配）
- 完全独立运营，不与其他工厂共享资源

线程（Thread）- 工厂里的生产线 
- 同一家工厂内的**多条并行生产线**
- 共享同一个厂房（共享进程内存），共用工厂的电力/水源（共享进程资源）
- 各自独立工作但能快速协作

- 进程创建开销大（需要分配独立资源），线程创建开销小（只需分配栈和寄存器）
- 进程间切换代价大，线程间切换代价小
- 进程通信方式复杂（管道/消息队列/共享内存等），线程通信方式简单（直接读写共享变量）
- 一个进程崩溃不影响其他进程，一个线程崩溃可能导致整个进程崩溃

### Nginx
高性能的Web服务器和反向代理服务器，把用户请求合理地分配到多台服务器上。
- 接待所有客户端请求
- 决定把请求安排到哪个后端服务器那里
- 同时还能处理很多管理工作（如静态文件服务、SSL加密等）
#### Nginx的负载均衡算法
1. 轮询（Round Robin）
	1. **工作原理**：像**排队点名**一样，按顺序把请求分配给每台服务器
	2. **优点**：简单公平
	3. **缺点**：不考虑服务器实际负载情况
	4. **适用场景**：所有服务器性能相近时
2. IP哈希（IP Hash）
	1. **工作原理**：根据客户IP地址计算一个固定值，总是**把同一个IP的请求发给同一台服务器**
	2. **优点**：能保持会话连续性（如购物车数据）
	3. **缺点**：如果某台服务器负载过重，不会自动调整
	4. **适用场景**：需要保持用户会话的应用
3. URL哈希（URL Hash）
	1. **工作原理**：根据请求的URL地址决定分配给哪台服务器
	2. **优点**：**相同URL的请求总是到同一服务器**，提高缓存效率
	3. **缺点**：URL分布不均可能导致负载不均
	4. **适用场景**：有大量静态资源需要缓存时
4. 最短响应时间（Least Time）
	1. **工作原理**：选择当前响应**最快的**服务器
	2. **优点**：能动态适应服务器负载变化
	3. **缺点**：实现相对复杂
	4. **适用场景**：服务器性能差异较大时
5. 加权轮询（Weighted Round Robin）
	1. **工作原理**：给**性能好的**服务器更高权重，让它处理更多请求
	2. **优点**：能充分利用高性能服务器
	3. **缺点**：需要手动设置权重
	4. **适用场景**：服务器配置不一时

#### Nginx位于七层网络结构中的哪一层
第7层（应用层），Nginx是七层负载均衡。
- 它能理解HTTP协议的内容（URL、Header等）
- 可以根据请求的具体内容做智能分配
- 相比工作在更低层（如第4层传输层）的负载均衡器更灵活

## Docker
### Docker底层实现
Source: https://xiaolincoding.com/backend_interview/internet_medium/tencent_cloud_intelligence.html#docker
- **基于Namespace的视图隔离**
	- Docker利用Linux命名空间（Namespace）来实现不同容器之间的隔离。
	- 每个容器都运行在自己的一组命名空间中，包括PID（进程）、网络、挂载点、IPC（进程间通信）等。
	- 这样，容器中的进程只能看到自己所在命名空间内的进程，而不会影响其他容器中的进程。
- **基于cgroups的资源隔离**
	- cgroups是Linux内核的一个功能，允许在进程组之间分配、限制和优先处理系统资源，如CPU、内存和磁盘I/O。
	- 它们提供了一种机制，用于管理和隔离进程集合的资源使用，有助于资源限制、工作负载隔离以及在不同进程组之间进行资源优先处理。

## MQ消息队列
Source: https://xiaolincoding.com/interview/mq.html#%E6%B6%88%E6%81%AF%E9%98%9F%E5%88%97%E5%9C%BA%E6%99%AF
MQ的本质包含: 生产者 (发消息) -> 队列 (存消息) -> 消费者 (消费消息)
### Kafka
- Kafka 是一个分布式流式处理平台。
	- 流平台: 
		- 消息队列：发布和订阅消息流，类似于消息队列。
		- 持久存储记录消息流：Kafka 会把消息持久化到磁盘，有效避免了消息丢失的风险。
		- 流式处理平台：在消息发布的时候进行处理，Kafka 提供了一个完整的流式处理类库。
Kafka特点如下：
- 高吞吐量、低延迟：kafka每秒可以处理几十万条消息，它的延迟最低只有几毫秒，每个topic可以分为多个partition, consumer group 对partition进行consumer操作。
- 可扩展性：kafka集群支持热扩展
- 持久性、可靠性：消息被持久化到本地磁盘，并且支持数据备份防止数据丢失
- 容错性：允许集群中节点失败（若副本数量为n,则允许n-1个节点失败）
- 高并发：支持数千个客户端同时读写

#### kafka的优势 (over RocketMQ/RabbitMQ)
- 性能：基于 Scala 和 Java 语言开发，设计中大量使用了批量处理和异步的思想，最高可以每秒处理千万级别的消息。
- 生态系统兼容性：与周边生态系统的兼容性好，尤其在大数据和流计算领域。

#### Kafka为什么这么快？
把Kafka想象成一个高效物流系统：
- **顺序写入优化**: 所有新消息都按顺序写入磁盘，磁盘只需一直往后放，速度超快。
	- 减少磁盘的寻道时间: 这种方式比随机写入更高效，因为磁盘读写头在顺序写入时只需移动一次。  
- **批量处理技术**: 攒够一批消息再一次性发送，减少网络开销和磁盘I/O操作的次数。
	- Kafka支持批量发送消息，这意味着生产者在发送消息时可以等待直到有足够的数据积累到一定量，然后再发送。这种方法减少了网络开销和磁盘I/O操作的次数，从而提高了吞吐量。  
- **零拷贝技术**: 数据直接从磁盘→网卡，跳过中间步骤，减少CPU和内存的负担，传输速度up。
	- 普通数据传输：从磁盘 → 内存 → 应用程序 → 内存 → 网卡
	- Kafka使用*零拷贝*技术，可以直接将数据从磁盘发送到网络套接字，避免了在用户空间和内核空间之间的多次数据拷贝。这大幅降低了CPU和内存的负载，提高了数据传输效率。  
- **压缩技术**
	- Kafka支持对消息进行压缩，*这不仅减少了网络传输的数据量，还提高了整体的吞吐量*。

## Coding - 打印金字塔/钻石+测试
```Implementation
class ShapePrinter {
    // 打印金字塔
    public static void printPyramid(int n) {
        for (int i = 1; i <= n; i++) {
            // 打印空格
            for (int j = 0; j < n - i; j++) { System.out.print(" "); }
            // 打印星號
            for (int j = 0; j < 2 * i - 1; j++) { System.out.print("*"); }
            System.out.println();
        }
    }

    // 打印鑽石
    public static void printDiamond(int n) {
        // 打印上半部分
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < n - i; j++) { System.out.print(" "); }
            for (int j = 0; j < 2 * i - 1; j++) { System.out.print("*"); }
            System.out.println();
        }
        
        // 打印下半部分
        for (int i = n - 1; i >= 1; i--) {
            for (int j = 0; j < n - i; j++) { System.out.print(" "); }
            for (int j = 0; j < 2 * i - 1; j++) { System.out.print("*"); }
            System.out.println();
        }
    }
}

public class Main
{
	public static void main(String[] args) {
		int n = 5;
        System.out.println("金字塔:");
        ShapePrinter.printPyramid(n);

        System.out.println("\n鑽石:");
        ShapePrinter.printDiamond(n);
	}
}

```
---
```Test Case
// IntelliJ: `src/test/java` 資料夾中建立 `ShapePrinterTest.java` -> JUnit
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShapePrinterTest {
    // 測試金字塔的行數是否正確
    @Test
    public void testPrintPyramid() {
        // **重定向系统输出**：
		// 1. 创建一个 `ByteArrayOutputStream` 对象 `outContent`，用来捕获程序的输出
        var outContent = new java.io.ByteArrayOutputStream();
		// 2. 使用 `System.setOut` 将系统的标准输出(控制台输出)重定向到这个流中
		PrintStream originalOut = System.out;
        System.setOut(new java.io.PrintStream(outContent));

		// 3. 调用真正要测试的方法，打印3行的金字塔。
        ShapePrinter.printPyramid(3);

		// 4. 断言：
		// 4.1. `expectedOutput` 定义了我们期望的输出结果        
        String expectedOutput = "  *\n ***\n*****\n";
        // 4.2. `assertEquals` 将实际输出(`outContent.toString()`)与期望输出比较，如果不一致则测试失败
        assertEquals(expectedOutput, outContent.toString());
        
        System.setOut(originalOut); // 還原
    }

    // 測試鑽石的行數是否正確
    @Test
    public void testPrintDiamond() {
        // 使用System.setOut來捕獲打印輸出
        var outContent = new java.io.ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new java.io.PrintStream(outContent));
        
        ShapePrinter.printDiamond(3);
        
        String expectedOutput = "  *\n ***\n*****\n ***\n  *\n";
        assertEquals(expectedOutput, outContent.toString());
        
        System.setOut(originalOut); // 還原
    }
}
```

## Test - General Concept + Case Study
Source: https://vuejs.org/guide/scaling-up/testing.html

### Testing Pyramid Structure
- Unit tests (fastest), integration tests (balanced), and E2E tests (slow but crucial)

### Unit Test 单元测试
- Goal: 验证小的、独立的代码单元是否按预期工作。
- Target: 一个单元测试通常覆盖一个单个函数、类、组合式函数或模块，不涉及 UI 渲染、网络请求或其他环境问题。
- Tool: Vitest @vue/test-utils
单元测试侧重于逻辑上的正确性，只关注应用整体功能的一小部分。他们可能会模拟你的应用环境的很大一部分（如初始状态、复杂的类、第三方模块和网络请求）。

#### Whitebox 白盒
知晓一个组件的实现细节和依赖关系。它们更专注于将组件进行更**独立**的测试。这些测试通常会涉及到模拟一些组件的部分子组件，以及设置插件的状态和依赖性（例如 Pinia）。
- 定义：**测试代码内部逻辑**（如分支、循环、逻辑覆盖）。
- 例子：检查代码中 `if-else` 分支是否全部覆盖，或循环是否可能死循环。
- 适用场景：单元测试、代码审查、安全性测试。
- 典型方法：语句覆盖、路径覆盖

#### Blackbox 黑盒
黑盒测试不知晓一个组件的实现细节。这些测试尽可能少地模拟，以测试组件在整个系统中的集成情况。它们通常会渲染所有子组件，因而会被认为更像一种“集成测试”。
- 定义：**不关心代码内部逻辑，只测试功能是否符合需求**（输入 → 输出是否正确）。
- 例子：测试登录功能时，只验证输入用户名密码后能否成功登录，不检查代码如何实现。
- 适用场景：功能测试、用户界面测试、兼容性测试。
- 典型方法：等价类划分、边界值分析

##### 边界值分析
测试输入范围的边界（最小值、最大值、略超出边界的情况），因为这里是Bug高发区。

### Component Test 组件测试
检查你的组件是否正常挂载和渲染、是否可以与之互动，以及表现是否符合预期。这些测试比单元测试导入了更多的代码，更复杂，需要更多时间来执行。

组件测试应该像用户一样，通过与组件互动来测试组件和其子组件之间的交互。例如，组件测试应该像用户那样点击一个元素。组件测试应该捕捉组件中的 *prop、事件、提供的插槽、样式、CSS class 名、生命周期钩子，和其他相关的问题*。

Tool: Vitest @vue/test-utils

- 对于 **视图** 的测试：根据输入 prop 和插槽断言渲染输出是否正确。
- 对于 **交互** 的测试：断言渲染的更新是否正确或触发的事件是否正确地响应了用户输入事件。

### Integration Test 集成测试
- Goal: 用于验证应用程序的不同模块或组件是否能够正常协同工作 (interactions between units, e.g., APIs and databases, services and external dependencies)。
	- Example: if an API endpoint correctly fetches data from a database. 
- Tool: Jest, Mocha, pytest

### End-to-end (E2E) Test 端到端测试
- Goal: 单元测试和组件测试在部署到生产时，对应用整体覆盖的能力有限。因此，E2E测试针对的可以说是应用最重要的方面：当用户实际使用你的应用时发生了什么。
- Target: 检查跨越多个页面的功能，针对你的应用在生产环境下进行网络请求。这些测试通常需要建立一个数据库或其他后端。
	- 捕捉路由、状态管理库、顶级组件（常见为 App 或 Layout）、公共资源或任何请求处理方面的问题。E2E测试不导入任何 Vue 应用的代码，而是完全依靠在真实浏览器中浏览整个页面来测试你的应用。
	- 验证整个应用流程，包括UI、后端、数据库和外部服务。
- Use Case: E2E测试和相应开发过程的主要问题之一是，运行整个套件需要很长的时间。通常情况下，这*只在持续集成和部署（CI/CD）管道中进行*。
- Tool: Playwright (support *Component Test*) / Cypress (Graph UI & support *Component Test*)
- 对于验证关键用户旅程至关重要，但由于维护和执行成本较高，应谨慎使用。

### Tool - Postman
用Postman测试HTTP接口？
Postman的核心用途是模拟请求、验证响应，适合接口功能测试和自动化初学。
1. **发送GET请求**：
    - 输入URL（如 `https://api.example.com/users`）；
    - 点击“Send”，检查返回状态码（200表示成功）和数据格式（JSON/XML）。
2. **测试异常情况**：
    - 修改参数为非法值（如`user_id=-1`），检查是否返回4xx错误码。
3. **自动化断言**：
    - 在Postman的“Tests”标签页写脚本，例如：
	    - 自动化验证 HTTP 请求的返回状态码是否为 200
	    - `pm.test("Status code is 200", () => pm.response.to.have.status(200));`

### Test Case Study
#### 登录页面
假设有一个登录页面，包含用户名、密码输入框和登录按钮，请设计测试用例（至少5条）。
1. 合法输入
	1. 步骤：已注册的用户名和正确的密码，点击登录按钮。
	2. 预期：登录成功，跳转到用户主页或仪表盘。
2. 错误密码（功能验证）
	1. 步骤：输入正确的用户名，但密码错误（如`123456`），点击登录。
	2. 预期：提示“用户名或密码错误”，不跳转页面。
3. 空输入（边界值）
	1. 步骤：不输入用户名或密码，直接点击登录按钮。
	2. 预期：提示“请输入用户名/密码”，并高亮标记空输入框。
4. SQL注入攻击（安全性）
	1. 步骤：在用户名输入框输入`' OR '1'='1`，密码任意输入。
	2. `SELECT * FROM users WHERE username = '' OR '1'='1' AND password = 'anything'`
	3. 预期：登录失败，提示错误信息，且系统未暴露数据库报错。
5. 密码掩码显示（用户体验）
	1. 步骤：输入密码时（如输入`abc123`）。
	2. 预期：密码显示为掩码（如`••••••`），而非明文。
6. 补充：用户名长度超限、密码大小写敏感、多次失败后锁定账户等。

#### 购物车
如果测试一个电商网站的“购物车”功能，你会关注哪些测试点？

思路：围绕核心功能（增删改查）、数据一致性、并发操作、兼容性等展开。
1. 基础功能（增删改查）
	1. 添加商品到购物车：验证商品信息（名称、价格、数量）是否正确显示。
	2. 删除商品：删除后购物车总价是否实时更新。
	3. 修改数量：输入负数、0、超大数（如9999）时的处理（应限制合理范围）。
2. 数据一致性
	1. 商品库存变化：若购物车中商品库存售罄，是否提示“缺货”。
	2. 价格同步：商品降价/涨价后，购物车内价格是否更新（或提示用户）。
3. 用户场景
	1. 未登录用户：添加商品后，登录后购物车内容是否保留。
	2. 多设备同步：手机端和PC端操作购物车，数据是否一致。
4. 并发与性能
	1. 高并发：多人同时抢购同一商品，购物车是否正确处理库存冲突。
	2. 大量商品：添加100+商品时，页面加载和结算是否流畅。    
5. 异常与边界
	1. 失效商品：购物车中商品下架后，是否标记“已失效”。
	2. 优惠券应用：使用优惠券后，总价计算是否正确（尤其是退款时）。
6. 扩展补充：
	1. 浏览器兼容性、移动端手势操作（如左滑删除）、与支付系统的衔接等。

#### 抖音点赞功能
思路：覆盖功能、并发、数据一致性、用户体验。
1. 基础功能
	1. 正常点赞：点击爱心图标，图标变红，点赞数+1。
	2. 取消点赞：再次点击，图标变灰，点赞数-1。
2. 边界与异常
	1. 重复快速点击：是否防抖（仅记录一次有效操作）。
	2. 点赞数显示上限：如显示“999+”而非实际数字。    
3. 数据一致性
	1. 用户A点赞后，用户B刷新页面是否实时看到更新。
	2. 删除视频后，关联点赞数据是否同步清除。
4. 并发与性能
	1. 万人同时点赞同一视频，计数器是否准确（需分布式锁）。
5. 安全性
	1. 未登录用户点击点赞，是否跳转到登录页。
	2. 接口防刷（如1分钟内限制100次点赞）。

#### 微信朋友圈发布功能
思路：覆盖内容类型、权限、兼容性、异常场景。
1. 内容输入验证
	1. 纯文本：长文本（1000字）、含Emoji、特殊符号（如`#@*`）。
	2. 图片/视频：9图上传、视频时长限制（如15秒）、格式支持（MP4/GIF）。
2. 权限控制
	1. 选择“仅自己可见”后，好友是否看不到该动态。
	2. 发布后修改权限，历史浏览者能否看到更新。
3. 异常场景
	1. 发布过程中断网：草稿是否自动保存。
	2. 发布内容含敏感词：是否提示“内容违规”。
4. 性能与兼容性
	1. 同时上传多张高清图，是否压缩或卡顿。
	2. 不同机型（iOS/Android）显示排版是否一致。

#### 天气预报 - 测试“切换城市”功能
1. **正常流程**: 输入“北京” → 显示北京天气
2. **异常输入**: 输入“@#￥%” → 提示“城市不存在”
3. **边界情况**: 输入超长城市名（如50个字符）
4. **网络延迟**: 切换城市时断网 → 显示“网络异常”
5. **数据一致性**: 切换城市后，实时天气和7天预报是否同步

#### IP是否合法
**问题分析**：IP合法性需满足格式（IPv4/IPv6）和数值范围，需考虑边界值和异常输入。

IPv4地址的合法性规则：
1. **格式**：由4个用点分隔的十进制数组成，例如 `192.168.1.1`。
2. **数值范围**：
    - 每个部分必须是0~255之间的整数。
    - 不能有前导零（比如 `012` 是非法的，除非是 `0`本身）。
    - 不能为空（即 `..` 是非法的）。        
3. **长度**：必须是4部分，不能多也不能少。

IPv6地址的合法性规则：
1. **格式**：由8组用冒号分隔的十六进制数组成，如 `2001:0db8:85a3:0000:0000:8a2e:0370:7334`。
2. **数值范围**：
    - 每组是1~4位的十六进制数（数字0-9，字母a-f或A-F）。
    - 可以省略前导零（比如 `0db8` 可以写成 `db8`）。
    - 可以用 `::` 表示连续的零组（但只能出现一次）。
3. **长度**：
    - 完整形式是8组，但 `::` 可以压缩连续的零组。
    - 压缩后至少要有1组（比如 `::1`  - 压缩开头零，是合法的）。

测试用例设计：
1. 合法输入（正常情况）。
2. 非法输入（格式错误、数值越界、特殊字符等）。
3. 边界值（IPv4的`0.0.0.0`和`255.255.255.255`，IPv6的压缩形式等）。
4. 异常输入（空值、非IP字符串、多余分隔符等）。

```sample test
import unittest
import re

def is_valid_ipv4(ip):
    """检查是否为合法的IPv4地址"""
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))

def is_valid_ipv6(ip):
    """检查是否为合法的IPv6地址（支持压缩形式）"""
    # 正则解释：允许1-4位十六进制数，支持::压缩（但仅能出现一次）
    pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::([0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,6}::([0-9a-fA-F]{1,4})?$'
    return bool(re.match(pattern, ip))

def is_valid_ip(ip):
    """综合判断IP（IPv4或IPv6）"""
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)

class TestIPValidation(unittest.TestCase):
    # IPv4测试用例
    def test_valid_ipv4(self):
        valid_ips = ["192.168.1.1", "0.0.0.0", "255.255.255.255"]
        for ip in valid_ips:
            self.assertTrue(is_valid_ipv4(ip), f"{ip} 应判定为合法IPv4")

    def test_invalid_ipv4(self):
        invalid_ips = ["256.1.1.1", "192.168.01.1", "192.168..1", "192.168.1", "a.b.c.d", ""]
        for ip in invalid_ips:
            self.assertFalse(is_valid_ipv4(ip), f"{ip} 应判定为非法IPv4")

    # IPv6测试用例
    def test_valid_ipv6(self):
        valid_ips = [
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "2001:db8:85a3::8a2e:370:7334",
            "::1",
            "ff02::1"
        ]
        for ip in valid_ips:
            self.assertTrue(is_valid_ipv6(ip), f"{ip} 应判定为合法IPv6")

    def test_invalid_ipv6(self):
        invalid_ips = [
            "2001::85a3::8a2e",  # 多个::
            "2001:0gb8:85a3::8a2e",  # 非法字符g
            ":::",
            ""  # 空字符串
        ]
        for ip in invalid_ips:
            self.assertFalse(is_valid_ipv6(ip), f"{ip} 应判定为非法IPv6")

    # 综合测试（IPv4或IPv6）
    def test_valid_ip(self):
        valid_ips = ["192.168.1.1", "::1"]
        for ip in valid_ips:
            self.assertTrue(is_valid_ip(ip), f"{ip} 应判定为合法IP")

    def test_invalid_ip(self):
        invalid_ips = ["256.1.1.1", "2001::85a3::8a2e", "not_an_ip"]
        for ip in invalid_ips:
            self.assertFalse(is_valid_ip(ip), f"{ip} 应判定为非法IP")

if __name__ == "__main__":
    unittest.main()
```

### Test情景模拟
#### 定位和复现 - 用户反馈“提交订单后页面卡死”
“卡死”可能是前端性能问题、接口超时或死锁，需结合日志和工具逐步缩小范围。
1. **收集信息**：
    - 用户的操作步骤（如点击“提交”按钮前的操作）；
    - 用户的环境（浏览器版本、网络状态）。
2. **尝试复现**：
    - 按照用户描述的操作路径测试；
    - 模拟弱网环境（Chrome开发者工具 → Network → Throttling）。
3. **排查方向**：
    - 前端：检查浏览器控制台是否有JavaScript报错；
    - 后端：查看接口响应是否超时（用Postman测试接口）；
    - 数据库：订单数据是否过大导致查询慢。

#### 测试时间不够
1. **优先级排序**：
    - 先测核心功能（如支付、登录），非核心功能（如UI动画）延后。
2. **风险导向**：
    - 重点测试历史Bug多的模块。
3. **自动化辅助**：
    - 用已有自动化脚本覆盖回归测试。

#### 如何与开发沟通Bug？
1. **标题**：清晰描述现象（如“登录页输入空格密码仍能登录”）；
2. **步骤**：详细复现路径；     
3. **证据**：截图、日志、视频。

#### 开发认为Bug不重要，但你坚持要修复
测试工程师是用户代言人，需平衡开发效率和用户体验。
1. **用数据说话**：
    - 提供复现步骤、截图/日志；
    - 说明影响范围（如“30%用户会遇到”）。
2. **从用户角度解释**：
    - 例如：“这个UI错位会导致移动端用户无法点击按钮，流失率增加。”
3. **寻求第三方意见**：
    - 拉上产品经理或测试组长一起评估优先级。

## 反问
下轮面试方向及入职负责任什么工作
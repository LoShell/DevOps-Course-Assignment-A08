# E8—E9 分工与个人贡献

以下为本轮分工与已回传进度。每人均需完成 A 轨 E8/E9 基线，不能以专项分工代替完整实验。

| 成员 | E8 主责 | E9 主责 | 专项文件名 | PR/实际结果 |
| --- | --- | --- | --- | --- |
| 刘馨雅 241250088（组长） | 基线来源、对象目标投影、未变输入复用；helper间接包含 | 函数体复用、已有头文件失效、集成与CI | integration | [PR #23](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/23)已合并，个人E8回归8项/E9回归9项；四轮个人及两轮集成原包核验通过 |
| 邱莉扉 241250097 | 声明图与helper共享头间接包含 | config.h/extra.h逐项声明修补，MD消除而RD保留 | declarations | [PR #25](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/25)已合并，定向2项/回归9项；E9个人包组长抽查通过 |
| 范从钰 241250071 | config.h间接include失效 | 间接头文件指令变化，边不变但应刷新 | include-invalidation | [PR #26](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/26)已合并，E8回归8项/E9回归9项；E9个人包组长抽查通过 |
| 叶原原 241250076 | helper间接包含及旧证据保持 | 配置刷新、拒绝、证据保持与恢复 | configuration-evidence | [PR #24](https://github.com/LoShell/DevOps-Course-Assignment-A08/pull/24)已合并，定向3项/回归10项；E9个人包组长抽查通过 |

合并记录：#24→83813593dfcd9ed181d1aa0e4ef4fecfc3670127；#25→bf59291d09473a6c072b4764231208f1bc93e3a7；#23→2a4abddf5d524459c4d1665262a13e33fc8c74ae；#26→04f386971d8f924cbdd85401c1f3583935c9b1c4。集成测试16项全部通过，见两阶段validation/INTEGRATED.md。个人历史测试数量与集成数量不混用。其他成员未抽查的E8/基线原包不标为组长独立核验；证据全集中下载及最终CI/平台交付仍待完成。

每人文件：labs/e8e10/test_student_<学号>.py、E8/records/<学号>.md、E9/records/<学号>.md、对应验收 CSV；专项为 E8/review/<专项文件名>.md 和 E9/review/<专项文件名>.md。课程三份模板保留在 docs/students/<学号>/e8-e10/，个人报告链接两阶段记录，避免重复维护实验结果。

所有成员还需按阶段自主任务完成新增用例。E8 的间接 include 可分别改变不同目标/嵌套深度/共享头/条件指令；E9 按分工扩展不同变化类型。至少写出独立预期，不以复制课程现有用例作为个人贡献。

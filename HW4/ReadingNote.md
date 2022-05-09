### Reading_Note

就自己presentation文献写一份读书报告
报告必须包含如下内容：

1. 介绍该论文的主要内容： 背景、方法、结果、结论等（约500字）
2. 评价该论文（约200字）

---

[Yang J, Yan R, Roy A, et al. The I-TASSER Suite: protein structure and function prediction[J]. Nature methods, 2015, 12(1): 7-8.](https://www.nature.com/articles/nmeth.3213)

​	目前已知的氨基酸序列数量要远远大于通过实验解析出来的蛋白质的三维结构的数量，也就是说并不是所有的氨基酸序列的三级结构都被解析出来了。所以对已知序列进行结构和功能的预测十分重要。

​	本文介绍的是使用 `I-TASSER Suite` 工具套件对蛋白质的三级结构和功能进行预测，流程如下;

1. 基于模板的穿线识别（threading template identification）
2. 结构的迭代装配仿真（iterative structure assembly simulation）
3. 模型选取与改进（model selection refinement）
4. 基于结构的功能注释（structure-based function annotation）

​	在展示部分，我负责分享2，3部分。

​	**第二部分**，根据第一部分穿线识别程序选出来的模板，第二部分将每个模板序列内部分成“穿线匹配区域”（`threading-aligned region`）和”穿线未匹配区域“（`threading-unaligned region`）。然后把”穿线匹配区域“直接装配为装配模型对应区域，”穿线未匹配区域“用从头预测（`ab initio folding`）的办法重构出序列的二级结构，然后再装配到装配模型对应部分。

​	装配过程主要想法：基于知识进行力场的构建，然后进行“副本交换的莫特卡罗“仿真实验（`replica-exchange Monte Carlo simulation`）。其中力场需要考虑到

1. 通用统计势能（`generic statical potentials`）
2. 氢键网络（`hydrogen-bonding network`）
3. 基于穿线的 `LOMETS` 约束（`threading-based restraints from LOMETS`）

​	**第三部分**，根据第二部分生成的装配模型根据最低自由能（`lowest free-energy`）选出模型，再对该模型进行二次模拟仿真以改进该模型的全局拓扑结构。最后进行“两步原子级别能量减小法”（`two-step atomic-level energy minimization approach`），对模型进行原子级别的优化。并在这部分提出新方法`ResQ`，来衡量模型残基级别的局部效果与B因子（`B factor`）。

​	最后作者给出了根据 `I-TASSER` 产生模型在 `TM-score` 和 `RMSD` 下有很好的表现。

---

​	本文主要是介绍作者提出来的新的蛋白质结构功能预测的算法流程。我所选两部分层次清晰，对新手友好。其次，本文附带该算法的实现——`I-TASSER Suit`程序，这一点非常好。
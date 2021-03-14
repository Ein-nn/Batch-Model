# Batch-Model
使用python等模块批量使用Modeller建模

1、结果文件夹的名称为其转运的对象，二级文件夹的名称为transporter的末尾id。
2、fasta格式文件为所有转运蛋白的序列文件，原本为1个包含所有序列的fasta文件，但因在批量建模中出现的中断情况，将其分为若干单独部分。
3、bat文件，类似于Linux中的shell文件，是win中在cmd里执行的脚本文件，用于调用modeller的库以配置python环境变量，并设置执行路径。mod_pattern.bat为python调用modeller建模的模板文件，mod.bat为针对每个序列单独调节参数和路径的命令行文件。
4、templates_information.txt为调用Bio.blast搜索木板时，记录的最优模板的coverage和identity信息。如下图所示，第一列为transporter的末尾id，第二列为匹配到的最优模板的id，第三列为模板匹配的coverage，第四列为模板匹配的identity。其中如果有些transporter没有模板或者模板的指标不合格（cover > 0.5 and ident > 0.2），则以“****”标记。

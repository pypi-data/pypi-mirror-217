import os
from KwoksNote.info import (welcome,how)
from KwoksNote.spider import (Browser)
from KwoksNote.function import (GetCityNumFromLiepin,
                                GetIpPool,
                                GetCityNumFromBossZhiPing,
                                GetCityNameFromLiepin,
                                YesOrNot,
                                CheckIp,
                                IntoZip,
                                ZipOut,
                                SendEmail,
                                GetEmail,
                                ProgressBar,
                                GetPlateSon,
                                GetPlateInfo,
                                MergeTable,
                                ChoiceColumn)
from KwoksNote.model import (GetProbMatrix,ToMat)
if not os.path.exists(
        r'C:\Windows\AgentPool.xlsx'):
    print('注意注意！\n请确保存在\'C:\Windows\AgentPool.xlsx\'的ip代理文件\n否则，ip池功能将无法使用\n继续使用请敲击回车键')
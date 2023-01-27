import os
import sys
from datetime import datetime


ALL = ["Desert_Eagle", "Dual_Berettas", "Five-SeveN", "Glock-18", "AK-47", "AUG", "AWP", "FAMAS", "G3SG1", "Galil_AR", "M249", "M4A4", "MAC-10", "P90", "UMP-45", "XM1014", "PP-Bizon", "MAG-7", "Negev", "Sawed-Off", "Tec-9", "P2000", "MP7", "MP9", "Nova", "P250", "SCAR-20", "SG_553", "SSG_08", "M4A1-S", "USP-S", "CZ75-Auto", "R8_Revolver"]
PISTOL = ["Glock-18", "USP-S", "Dual_Berettas", "Five-Seven", "Tec-9", "Desert_Eagle"]
HEAVY = ["Nova", "XM1014", "MAG-7", "M249", "Negev"]
SMG = ["MAC-10", "MP9", "MP7", "UMP-45", "P90", "PP-Bizon"]
RIFLE = ["Galil_AR", "FAMAS", "AK-47", "M4A1-S", "SSG_08", "AUG", "SG_553", "AWP", "SCAR-20"]
search = ["AWP", "AK-47"]


args = ""
login = sys.argv[1]
for weapon in search:
    args += weapon
    args += " "
start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#web_search.main(True,search)
code = "python web_search.py " + str(login) + " " + args
os.system(code)
end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print("started search:" + start + "\nended search:" + end)


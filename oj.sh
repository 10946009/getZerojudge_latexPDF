#!/bin/bash

# array=("A1_d049" "A2" "B_b877" "C_a038" "D_b130" "E_b162" "F_L1905" "G_e208" " H_e267" "I_c012" "J_PRIME1" "K_d120")
#array=("L_cses1146" "M_cses2205" "N_b032" " O_cses1636" "P_c126" "Q_ALDS1_7_B")
array=("I_c012")
for i in "${array[@]}"; do   # The quotes are necessary here
    echo ${i}
    # mkdir -p ~/Downloads/Pro202211/${i}/data/sample
    # mkdir -p ~/Downloads/Pro202211/${i}/data/secret
    # cp ./D_b130/data/sample/*.* ~/Downloads/Pro202211/${i}/data/sample/
    # cp ./D_b130/data/secret/*.* ~/Downloads/Pro202211/${i}/data/secret/
    # cp ./domjudge-problem.ini  ~/Downloads/Pro202211/${i}
    # cp ./problem.pdf ~/Downloads/Pro202211/${i}
    # cp ./problem.yaml ~/Downloads/Pro202211/${i}
    # cp ./ans.py ~/Downloads/Pro202211/${i}
    cd  ~/Downloads/LatexICPC2022/${i}
    zip -r ${i} . -x ".*" -x "__MACOSX"  -x "./data/.DS_Store" -x "${i}" -x "README.md"
    mv ~/Downloads/LatexICPC2022/${i}/${i}.zip ~/Downloads/Pro20221130/
done
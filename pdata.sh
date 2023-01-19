# array=("D_b130" "E_b162")
array=("CSES1636")
for i in "${array[@]}"; do   # The quotes are necessary here
    for string in ./${i}/dom/data/sample/*.in
    do
        string=${string%???}
        python3 ./${i}/code/${i}.py < ${string}.in > ${string}.ans
    done
    for string in ./${i}/dom/data/secret/*.in
    do
        string=${string%???}
        python3 ./${i}/code/${i}.py < ${string}.in > ${string}.ans
    done
    echo ${i}
    # python3 ./${i}/code/${i}.py < ./${i}/dom/data/sample/1.in > ./${i}/dom/data/sample/1.ans
    # python3 ./${i}/code/${i}.py < ./${i}/dom/data/sample/2.in > ./${i}/dom/data/sample/2.ans
    # echo "secret"
    # python3 ./${i}/code/${i}.py < ./${i}/dom/data/secret/6.in > ./${i}/dom/data/secret/6.ans
    # python3 ./${i}/code/${i}.py < ./${i}/dom/data/secret/7.in > ./${i}/dom/data/secret/7.ans
    # python3 ./${i}/${i}.py < ./${i}/data/secret/8.in > ./${i}/data/secret/8.ans
    # python3 ./${i}/${i}.py < ./${i}/data/secret/9.in > ./${i}/data/secret/9.ans
    # python3 ./${i}/${i}.py < ./${i}/data/secret/10.in > ./${i}/data/secret/10.ans
done
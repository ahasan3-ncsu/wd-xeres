set dirs p*/

for dir in $dirs
    cd $dir
    pwd

    set toml ballbox_*.toml
    echo $toml
    ../../RustBCA SPHEREINCUBOID $toml

    cd ..
    python ../scripts/xe_shell.py $dir/(string replace -r '\.toml$' '' $toml)
end

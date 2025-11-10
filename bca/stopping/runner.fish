set ion $argv[1]
cd $ion
pwd

for x in (seq 10)
    echo $x
    ../../RustBCA 0D umo_0D.toml
    python ../extractor.py umo_0D $ion
end

set -x
studyDir=/home/atom/research/wd-xeres/IRADINAGUI_WORKDIR/U_in_UMo
iradinaExe=/home/atom/research/wd-xeres/iradinaGUI/iradinaCode/iradina_linux64.exe
cd $studyDir
tree
ls -alt
( $iradinaExe -p 9 -data ../data -c ./Configuration.in  | tee ./iradina.log )&
# to see iradina progress
# tail -f /home/atom/research/wd-xeres/IRADINAGUI_WORKDIR/U_in_UMo/iradina.log

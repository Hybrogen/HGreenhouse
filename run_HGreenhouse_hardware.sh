ProcNumber=`ps aux|grep -w "python3 manage_greenhouse.py"|grep -v grep|wc -l`
if [ $ProcNumber -ne 0 ];then
   result=$ProcNumber
else
   result=0
   python3 manage_greenhouse.py
fi
# echo ${result}

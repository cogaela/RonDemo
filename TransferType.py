import sys
import os
import glob
import subprocess
import csv
failed = 0
def main():
    try:
        file = os.stat("Data File.csv")
        if file.st_size == 0:
            print "Data File is Empty"
    except OSError:
        print "Data File.csv not Found"
        sys.exit(1)

def compare(calllog1, transfertype1, y, gen_result):
    x = 0
    z = 0
    transfer = transfertype1.split(';')
    total_terms = len(transfer)
    global failed
    y = str(y)
    print "Test " + y + ": " + "For Call log " + calllog1
    total_terms = total_terms -1
    alllines = set()
    while total_terms > x :
        flag = 0
        split_1 = transfer[x].split('=')
        first = split_1[0].lower().strip()
        second = split_1[1].strip()
        with open(calllog1) as calllog:
            verbiage = set()
            for line in calllog:
                if (first +':' in line.lower() or first +'=' in line.lower()) and second in line:
                    verbiage.add(line)
                    alllines.add(line)
                    flag = 1
                elif first +':' in line.lower() or first +'=' in line.lower():
                    verbiage.add(line)
                    alllines.add(line)

        if flag == 0:
            print transfer[x] + "\tWrong Value"
            z = 1
        elif len(verbiage)==0:
            print transfer[x] + "\tNot Found"
            z = 1
        else:
            print transfer[x] + "\tFound"
        print ''.join(verbiage)
        x += 1
    verbi = '<br/>'.join(alllines)
    prompi = '<br/>'.join(transfer)
    if z == 1:
        print "                   STATUS: FAILED"
        gen_result.write(
            "<tr><td>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td> <td bgcolor='#e06745'>Failed</td>  <td>" + calllog1 + "</td></tr>")

    else:
        print "                   STATUS: PASSED"
        gen_result.write(
            "<tr><td>" + y + "</td><td>" + prompi + "</td> <td>" + verbi + "</td> <td bgcolor='#99e26f'>Passed</td>  <td>" + calllog1 + "</td></tr>")


def excel():
    gen_result = open("result.html", "a")
    gen_result.write("<html><table align ='center' border='1' width='70%'> <h1>Build Acceptance Test</h1> <p>Transfer Term</p>")
    z= 0
    with open('Data File.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        y= 1;
        gen_Report.write("<tr><td> Test Case </td> "
                         "<td> Transfer Term </td> "
                         "<td> Actual Logs </td> "
                         "<td> Result </td> "
                         "<td>Call Log </td></tr>")
        for line in reader:
            transfertype1 =line[1]
            calllog1 = line[2]
            if len(transfertype1) >= 5:
                if len(calllog1)>= 5:
                    compare(calllog1, transfertype1, y, gen_result)
                    y+=1

if __name__ == "__main__":

    main()
    excel()
    if failed == 1:
        print"\n\n\n"
        raise SystemError('One of the Test Cases Failed')

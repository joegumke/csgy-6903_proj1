import performanceMetric as performanceMetric

def main():

    file1 = "../main.resources/test2dict_40.txt"
    file2 = "../main.resources/test2dict_400.txt"
    file3 = "../main.resources/test2dict_4000.txt"

    performanceMetric.measurePerformance(file1, file2, file3)


if __name__=="__main__":
    main()
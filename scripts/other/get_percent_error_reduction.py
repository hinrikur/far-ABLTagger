import sys


if __name__ == '__main__':
    
    BEFORE = float(sys.argv[1])
    AFTER = float(sys.argv[2])
    
    accuracy_gain = AFTER - BEFORE
    
    error_before = BEFORE - 100.00
    error_after = AFTER - 100.00
    
    percentage_error_reduction = ((error_after - error_before) / abs(error_before))*100.00
    
    print(f'\nAccuracy before: {BEFORE}%')
    print(f'Accuracy after: {AFTER}%')
    
    print(f'Accuracy gain: {"%.2f" % round(accuracy_gain, 2)}%\n')
    
    print('Percentage error reduction:', "%.2f" % round(percentage_error_reduction, 2) + '%\n')

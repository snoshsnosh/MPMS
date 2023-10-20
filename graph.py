def ErrorDetect(input) :
    i = 0
    if input < 1 :
        while True :
            if 10**(-(i+1)) <= input < 10**(-i) :
                output = round(input, i+1)
                break
            i += 1
    else :
        while True :
            if 10**(i) <= input < 10**(i+1) :
                output = round(input, -(i))
                break
            i += 1
    return output


def WidthFunction(max, min, nn, option) : 
    loopmax = 0
    loopmin = 0
    if option != 0 :
        width = option
        if min >= 0 :
            while True :
                loopmax += 1
                if 0 < max < width*loopmax :
                    break
        if max <= 0 :
            while True : 
                loopmin += 1
                if -width*loopmin < min < 0 :
                    break
        if min*max < 0 :
            while True :
                loopmax += 1
                if 0 < max < width*loopmax :
                    break
            while True :
                loopmin += 1
                if -width*loopmin < min < 0 :
                    break
    else:
        if min >= 0 :
            width = max/nn
            width = ErrorDetect(width)
            while True :
                loopmax += 1
                if 0 < max < width*loopmax :
                    break
        if max <= 0 :
            width = abs(min)/nn
            width = ErrorDetect(width)
            while True : 
                loopmin += 1
                if -width*loopmin < min < 0 :
                    break
        if min*max < 0 :
            width = (max-min)/nn
            width = ErrorDetect(width)
            while True :
                loopmax += 1
                if 0 < max < width*loopmax :
                    break
            while True :
                loopmin += 1
                if -width*loopmin < min < 0 :
                    break
    return width, loopmax, loopmin


def PythonPlot(graphname, xdata, ydata, xlabel, ylabel, width_x, width_y, nn) :
    import numpy as np
    import matplotlib.pyplot as plt
    width_x, loopmax_x, loopmin_x = WidthFunction(max(xdata), min(xdata), nn, width_x)
    width_y, loopmax_y, loopmin_y = WidthFunction(max(ydata), min(ydata), nn, width_y)
    fsize = 18
    fsize_text = 15
    plt.rcParams['xtick.direction'] = 'in' 
    plt.rcParams['ytick.direction'] = 'in' 
    plt.rcParams["xtick.top"] = True
    plt.rcParams["xtick.bottom"] = True
    plt.rcParams["ytick.left"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["xtick.labelsize"] = fsize_text
    plt.rcParams["ytick.labelsize"] = fsize_text
    plt.rcParams["figure.figsize"] = (9, 6)
    fig1 , ax1 = plt.subplots ()
    curve1 = ax1.plot(xdata, ydata, marker='o', markersize=1, linestyle='None', c='blue')
    ax1.set_xlabel(xlabel, fontsize=fsize)
    ax1.set_ylabel(ylabel, fontsize=fsize)
    ax1.set_xlim(-width_x*loopmin_x, width_x*loopmax_x)
    ax1.set_ylim(-width_y*loopmin_y, width_y*loopmax_y)
    ax1.set_xticks(np.arange(-width_x*(loopmin_x), width_x*(loopmax_x+1), step=width_x))
    ax1.set_yticks(np.arange(-width_y*(loopmin_y), width_y*(loopmax_y+1), step=width_y))
    if loopmin_x != 0 :
        plt.axvline(x=0, color='black', linestyle='--')
    if loopmin_y != 0 :
        plt.axhline(y=0, color='black', linestyle='--')
    plt.savefig(graphname)
    plt.show()


def IgorPlot(outputfilename, xdata, ydata, xname, yname, xlabel, ylabel, width_x, width_y, nn) :
    width_x, loopmax_x, loopmin_x = WidthFunction(max(xdata), min(xdata), nn, width_x)
    width_y, loopmax_y, loopmin_y = WidthFunction(max(ydata), min(ydata), nn, width_y)
    fsize = 30
    setting = {
    'tick': 2,
    'mirror': 1,
    'font': 'Helvetica',
    'fSize': str(fsize),
    'zero' : 3,
    'width': '{Aspect,1.5}',
    # 'height': 600,
    'standoff': 0,
    # 'btLen': 8,
    # 'stLen': 4,
    # 'margin(top)': 30,
    # 'margin(right)': 30,
    # 'nticks(bottom)': 10,
    # 'nticks(left)': 10,
    'minor': 1,
    # 'manTick': 0,
    # 'highTrip(left)': 999999,
    # 'notation(left)': 1,
    # 'tickEnab(left)': '{-0.1,INF}',
    }
    sentence = ', '.join([f'{key}={val}' for key,val in setting.items()])
    with open(outputfilename, mode = 'w') as f:
        f.write(f'IGOR \n')
        f.write(f'WAVES/O ' + str(xname) + ', ' + str(yname) + ' \n')
        f.write('BEGIN \n')
        for i in range(len(xdata)):
            f.write(f'{xdata[i]} {ydata[i]} \n')
        f.write('END\n')
        f.write(f'X Display ' + str(yname) + ' vs ' + str(xname) + ' \n')
        f.write(f'X ModifyGraph {sentence} \n')
        f.write('X Label bottom "' + str(xlabel) + '" \n')
        f.write('X Label left "' + str(ylabel) + '" \n')
        f.write('X SetAxis bottom ' + str(-(width_x*loopmin_x)) + ', ' + str(width_x*loopmax_x) + ' \n')
        f.write('X SetAxis left ' + str(-(width_y*loopmin_y)) + ', ' + str(width_y*loopmax_y) + ' \n')


def PythonPlotDouble(graphname, xdata1, xdata2, ydata1, ydata2, ydata3, xlabel, ylabel1, ylabel2, width_x1, width_y1, width_y2, text, nn) :
    import numpy as np
    import matplotlib.pyplot as plt
    width_x1, loopmax_x1, loopmin_x1 = WidthFunction(max(xdata1), min(xdata1), nn, width_x1)
    width_x1, loopmax_x2, loopmin_x2 = WidthFunction(max(xdata2), min(xdata2), nn, width_x1)
    width_y1, loopmax_y1, loopmin_y1 = WidthFunction(max(ydata1), min(ydata1), nn, width_y1)
    width_y2, loopmax_y2, loopmin_y2 = WidthFunction(max(ydata2), min(ydata2), nn, width_y2)
    fsize = 18
    fsize_text = 15
    plt.rcParams['xtick.direction'] = 'in' 
    plt.rcParams['ytick.direction'] = 'in' 
    plt.rcParams["xtick.top"] = True
    plt.rcParams["xtick.bottom"] = True
    plt.rcParams["ytick.left"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["xtick.labelsize"] = fsize_text
    plt.rcParams["ytick.labelsize"] = fsize_text
    plt.rcParams["figure.figsize"] = (9, 6)
    fig1 , ax1 = plt.subplots ()
    ax2 = ax1.twinx()
    curve1 = ax1.plot(xdata1, ydata1, marker='o', markersize=1, linestyle='None', c='blue')
    curve2 = ax2.plot(xdata1, ydata2, marker='o', markersize=1, linestyle='None', c='red')
    curve3 = ax2.plot(xdata2, ydata3, marker='None', c='black')
    ax1.set_xlabel(xlabel, fontsize=fsize)
    ax1.set_ylabel(ylabel1, fontsize=fsize)
    ax2.set_ylabel(ylabel2, fontsize=fsize)
    if abs(max(xdata1)-min(xdata1)) > abs(max(xdata2)-min(xdata2)) :
        ax1.set_xlim(-width_x1*loopmin_x1, width_x1*loopmax_x1)
        ax1.set_xticks(np.arange(-width_x1*loopmin_x1, width_x1*(loopmax_x1+1), step=width_x1))
    else :
        ax1.set_xlim(-width_x1*loopmin_x2, width_x1*loopmax_x2)
        ax1.set_xticks(np.arange(-width_x1*loopmin_x2, width_x1*(loopmax_x2+1), step=width_x1))
    ax1.set_ylim(-width_y1*loopmin_y1, width_y1*loopmax_y1)
    ax2.set_ylim(-width_y2*loopmin_y2, width_y2*loopmax_y2)
    ax1.set_yticks(np.arange(-width_y1*(loopmin_y1), width_y1*(loopmax_y1+1), step=width_y1))
    ax2.set_yticks(np.arange(-width_y2*(loopmin_y2), width_y2*(loopmax_y2+1), step=width_y2))
    if loopmin_x1 != 0 or loopmin_x2 != 0 :
        plt.axvline(x=0, color='black', linestyle='--')
    ax1.text(x=0.45, y=0.15, s=text, c='black', ha='left', fontsize=fsize_text, transform=ax1.transAxes)
    plt.savefig(graphname)
    plt.show()

def IgorPlotDouble(outputfilename, xdata1, xdata2, ydata1, ydata2, ydata3, xname1, xname2, yname1, yname2, yname3, xlabel1, ylabel1, ylabel2, width_x1, width_y1, width_y2, text, nn) :
    width_x1, loopmax_x1, loopmin_x1 = WidthFunction(max(xdata1), min(xdata1), nn, width_x1)
    width_x1, loopmax_x2, loopmin_x2 = WidthFunction(max(xdata2), min(xdata2), nn, width_x1)
    width_y1, loopmax_y1, loopmin_y1 = WidthFunction(max(ydata1), min(ydata1), nn, width_y1)
    width_y2, loopmax_y2, loopmin_y2 = WidthFunction(max(ydata2), min(ydata2), nn, width_y2)
    fsize = 30
    setting = {
    'rgb(' + yname1 + ')' : (0,0,65535),
    'mode(' + yname1 + ')' : 3,
    'marker(' + yname1 + ')' : 19,
    'msize(' + yname1 + ')' : 2,
    'mode(' + yname2 + ')' : 3,
    'marker(' + yname2 + ')' : 19,
    'msize(' + yname2 + ')' : 2,
    'rgb(' + yname3 + ')' : (0,0,0),
    'lsize(' + yname3 + ')' : 2,
    'tick': 2,
    'mirror(bottom)': 1,
    'font': 'Helvetica',
    'fSize': str(fsize),
    'zero(bottom)' : 3,
    'width': '{Aspect,1.5}',
    # 'height': 600,
    'standoff': 0,
    # 'btLen': 8,
    # 'stLen': 4,
    # 'margin(top)': 30,
    # 'margin(right)': 30,
    # 'nticks(bottom)': 10,
    # 'nticks(left)': 10,
    'minor': 1,
    # 'manTick': 0,
    # 'highTrip(left)': 999999,
    # 'notation(left)': 1,
    # 'tickEnab(left)': '{-0.1,INF}',
    }
    sentence = ', '.join([f'{key}={val}' for key,val in setting.items()])
    with open(outputfilename, mode = 'w') as f:
        f.write(f'IGOR \n')
        f.write(f'WAVES/O {xname1}, {yname1}, {yname2} \n')
        f.write('BEGIN \n')
        for i in range(len(xdata1)):
            f.write(f'{xdata1[i]} {ydata1[i]} {ydata2[i]} \n')
        f.write('END\n')
        f.write(f'WAVES/O {xname2}, {yname3} \n')
        f.write('BEGIN \n')
        for i in range(len(xdata2)):
            f.write(f'{xdata2[i]} {ydata3[i]} \n')
        f.write('END\n')
        f.write(f'X Display {yname1} vs {xname1} \n')
        f.write(f'X AppendToGraph/R {yname2} vs {xname1} \n')
        f.write(f'X AppendToGraph/R {yname3} vs {xname2} \n')
        f.write(f'X ModifyGraph {sentence} \n')
        f.write('X Label bottom "' + xlabel1 + '" \n')
        f.write('X Label left "' + ylabel1 + '" \n')
        f.write('X Label right "' + ylabel2 + '" \n')
        f.write('X TextBox/C/N=text0/F=0 "' + text + '" \n')
        if abs(max(xdata1)-min(xdata1)) > abs(max(xdata2)-min(xdata2)) :
            f.write('X SetAxis bottom ' + str(-(width_x1*loopmin_x1)) + ', ' + str(width_x1*loopmax_x1) +' \n')
        else :
            f.write('X SetAxis bottom ' + str(-(width_x1*loopmin_x2)) + ', ' + str(width_x1*loopmax_x2) +' \n')
        f.write('X SetAxis left ' + str(-(width_y1*loopmin_y1)) + ', ' + str(width_y1*loopmax_y1) + ' \n')
        f.write('X SetAxis right ' + str(-(width_y2*loopmin_y2)) + ', ' + str(width_y2*loopmax_y2) + ' \n')

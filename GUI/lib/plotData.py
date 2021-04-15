# Copyright (c) 2021 Adrien Pajon (adrien.pajon@gmail.com)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# import numpy as np
import np.genfromtxt, np.divide, np.cumsum, np.argwhere
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from api_phidget_n_MQTT.src.lib_global_python import searchLoggerFile


def PlotData(config):
    ############
    # Encoder's resolution in mm per pulse
    #     Encoder_mm_per_Pulse = 0.02
    Encoder_mm_per_Pulse = config.getfloat('encoder', 'resolution')
    print("encoder resolution : " + str(Encoder_mm_per_Pulse))

    ############
    # search for the last logger file based on the indentation
    #     filename="Logger_encoder_07.txt"
    filename = searchLoggerFile.searchLoggerFile(config)
    print(filename)
    try:
        data = np.genfromtxt(filename, delimiter=",", names=True)
    except:
        return False
    # convert the number of pulse position change into mm
    PositionChange_mm = data['PositionChange'] * Encoder_mm_per_Pulse

    # recorded time when datas are received in s
    time = data['TimeRecording']
    time -= time[0]  # the beginning time at 0

    # vel is the velocity measured by the encoder
    # as the positionChange_mm is in mm and the TimeChange is in ms
    # the velocity is given in m/s
    # If a 'detach' from the encoder, TimeChange=0 and vel will be Inf
    vel = np.divide(PositionChange_mm, data['TimeChange'])

    ############
    # initialize the plot
    fig, ax1 = plt.subplots()

    # plot the encoder velocity in time
    color = 'tab:blue'
    lns1 = ax1.plot(time, vel, label="Velocity", color=color)
    ax1.set_xlabel("time[s]")
    ax1.set_ylabel("Velocity[m/s]", color=color)

    color = 'tab:blue'
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid()

    #     # Create a Rectangle patch
    #     rect = patches.Rectangle((0,0),20,0.2,linewidth=1,edgecolor='k',facecolor='tab:grey')
    #     # Add the patch to the Axes
    #     ax1.add_patch(rect)

    # Draw a grey rectangle patch for each detach of the encoder aka 'missing values' aka TimeChange=0
    for k in np.argwhere(data['TimeChange'] == 0):
        if k == 0:
            rect = patches.Rectangle((time[k], 0), time[k + 1] - time[k], 2, linewidth=1, edgecolor='k',
                                     facecolor='tab:grey')
            ax1.add_patch(rect)
            lns3 = rect
        elif k != len(data['TimeChange']):
            if k == np.argwhere(data['TimeChange'] == 0)[0]:
                rect = patches.Rectangle((time[k - 1], 0), time[k + 1] - time[k - 1], 2, linewidth=1, edgecolor='k',
                                         facecolor='tab:grey')
                lns3 = ax1.add_patch(rect)
            else:
                rect = patches.Rectangle((time[k - 1], 0), time[k + 1] - time[k - 1], 2, linewidth=1, edgecolor='k',
                                         facecolor='tab:grey')
                ax1.add_patch(rect)

    # plot the encoder distance measured in m
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Position[m]', color=color)  # we already handled the x-label with ax1
    lns2 = ax2.plot(time, np.cumsum(PositionChange_mm / 1000), color=color, label="Position")
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("velocity and position measured by encoder \n in file : " + filename)

    # Legend manage if there is no missing value meaning lns3 does not exist
    try:
        lns = [lns1[0], lns2[0], lns3]
        labs = ('Velocity', 'Position', 'Missing velocity')
    except:
        lns = [lns1[0], lns2[0]]
        labs = ('Velocity', 'Position')
    ax1.legend(lns, labs)  # , loc=0)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    return True

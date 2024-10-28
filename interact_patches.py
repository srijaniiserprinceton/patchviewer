import numpy as np
import matplotlib.pyplot as plt; plt.ion()
from matplotlib.widgets import Slider, Button, RadioButtons

if __name__ == '__main__':
    # the sample time (or longitude) series we want to color
    Ntimes = 999
    t = np.linspace(0, 1, Ntimes)
    y1 = np.sin(6 * np.pi * t)

    # the number of plasma paramters
    Nparams = 1

    # the estimated number of patches
    Npatches = 3

    #-------------------- setting up the initial plots-------------------------------------#
    fig, ax = plt.subplots(Nparams, 1, figsize = (10, 4))

    # finding the indices between patches (anchor points)
    start_idx = np.zeros((Nparams, Npatches))
    end_idx = np.zeros((Nparams, Npatches))

    # creating a dictionary of line elements to be used later
    lines = {}

    for param_idx in range(Nparams):
        lines[param_idx] = {}

        lines[param_idx]['start_idx'] = np.zeros(Npatches+1, dtype='int')
        lines[param_idx]['end_idx'] = np.zeros(Npatches+1, dtype='int')

        # initializing the starting and ending indices (equal gaps by default)
        start_idx = np.arange(Npatches) * (Ntimes // Npatches)
        end_idx = np.arange(1, Npatches+1) * (Ntimes // Npatches)
        end_idx[-1] = end_idx[-1] - 1

        lines[param_idx]['start_idx'][:-1] = start_idx
        lines[param_idx]['end_idx'][:-1] = end_idx

        lines[param_idx]['start_idx'][-1] = end_idx[-1]
        lines[param_idx]['end_idx'][-1] = -1

        for patch_idx in range(Npatches+1):
            idx1, idx2 = lines[param_idx]['start_idx'][patch_idx],\
                         lines[param_idx]['end_idx'][patch_idx]

            if(patch_idx == 0):
                [lines[param_idx][-1]] = ax.plot(t, y1, 'k', alpha=0.4)
                [lines[param_idx][patch_idx]] = ax.plot(t[idx1:idx2], y1[idx1:idx2], lw=2)
            elif(patch_idx == Npatches):
                [lines[param_idx][patch_idx]] = ax.plot(t, y1, 'k', alpha=0.0)
            else:
                [lines[param_idx][patch_idx]] = ax.plot(t[idx1:idx2], y1[idx1:idx2], lw=2)

    #---------------------- setting up the interactive widget ---------------------------------#
    # Define an axes area and draw a slider in it
    axis_color = 'black'
    fig.subplots_adjust(left=0.2, right=0.98, bottom=0.15, top=0.98)

    patch_sliders = {}

    for param_idx in range(Nparams):
        patch_sliders[param_idx] = {}
        for patch_idx in range(Npatches+1):
            index_slider_ax  = fig.add_axes([0.01 + 0.03*patch_idx, 0.2, 0.01, 0.7], facecolor='black')
            index_slider = Slider(index_slider_ax, f'P{patch_idx}', 0, Ntimes, color='k', valstep=1,
                                  valinit=lines[param_idx]['start_idx'][patch_idx], orientation='vertical')
            patch_sliders[param_idx][patch_idx] = index_slider

    # Define an action for modifying the line when any slider's value changes
    def sliders_on_changed(val):
        for param_idx in range(Nparams):
            for patch_idx in range(Npatches+1):
                updated_start_idx = int(patch_sliders[param_idx][patch_idx].val)
                if(patch_idx == Npatches): updated_end_idx = -1
                else: updated_end_idx = int(patch_sliders[param_idx][patch_idx+1].val)

                lines[param_idx]['start_idx'][patch_idx] = updated_start_idx
                lines[param_idx]['end_idx'][patch_idx] = updated_end_idx

                idx1, idx2 = lines[param_idx]['start_idx'][patch_idx],\
                             lines[param_idx]['end_idx'][patch_idx]

                lines[param_idx][patch_idx].set_data(t[idx1:idx2], y1[idx1:idx2])

                fig.canvas.draw_idle()

    # updating the plots whenever sliders are changed
    for param_idx in range(Nparams):
        for patch_idx in range(Npatches+1):
            patch_sliders[param_idx][patch_idx].on_changed(sliders_on_changed)

    # Add a button for resetting the parameters
    reset_button_ax = fig.add_axes([0.85, 0.025, 0.1, 0.04])
    reset_button = Button(reset_button_ax, 'Reset', color='yellow', hovercolor='0.1')
    def reset_button_on_clicked(mouse_event):
        for param_idx in range(Nparams):
            for patch_idx in range(Npatches+1):
                patch_sliders[param_idx][patch_idx].reset()

    reset_button.on_clicked(reset_button_on_clicked)

            
        
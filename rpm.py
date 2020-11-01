import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import cv2
def motor_rmp(value):
    # Generate universe variables
    volt = np.arange(0, 6, 1)
    rpm = np.arange(0, 500, 100)


    # Generate fuzzy membership functions for input
    i_null = fuzz.trimf(volt, [0, 0, 1])
    i_zero = fuzz.trimf(volt, [0, 1, 2])
    i_small = fuzz.trimf(volt, [1, 2, 3])
    i_medium = fuzz.trimf(volt, [2, 3, 4])
    i_large = fuzz.trimf(volt, [3,4,5])
    i_very_large = fuzz.trimf(volt, [4, 5, 5])

    # Output membership function

    o_zero = fuzz.trimf(rpm, [0, 0, 100])
    o_small = fuzz.trimf(rpm, [0,100,200])
    o_medium = fuzz.trimf(rpm, [100, 200, 300])
    o_large = fuzz.trimf(rpm, [200,300,400])
    o_very_large = fuzz.trimf(rpm, [300, 400, 400])

    # membership value calculation using the value
    volt_level_null = fuzz.interp_membership(volt, i_null, value)
    volt_level_zero = fuzz.interp_membership(volt, i_zero, value)
    volt_level_small = fuzz.interp_membership(volt, i_small, value)
    volt_level_medium = fuzz.interp_membership(volt, i_medium, value)
    volt_level_large = fuzz.interp_membership(volt, i_large, value)
    volt_level_very_large = fuzz.interp_membership(volt, i_very_large, value)

    active_rule1 = np.fmax(volt_level_null, volt_level_zero)
    rpm_activation_zero = np.fmin(active_rule1,o_zero)
    rpm_activation_small = np.fmin(volt_level_small, o_small)
    rpm_activation_medium = np.fmin(volt_level_medium, o_medium)
    rpm_activation_large = np.fmin(volt_level_large, o_large)
    rpm_activation_very_large = np.fmin(volt_level_very_large, o_very_large)

    rmp_dummy = np.zeros_like(rpm)
    aggregated = np.fmax(rpm_activation_zero, np.fmax(rpm_activation_small, np.fmax(rpm_activation_medium,np.fmax(rpm_activation_large,rpm_activation_very_large))))


    # Calculate defuzzified result
    rpm_out = fuzz.defuzz(rpm, aggregated, 'centroid')
    print(rpm_out)
    rpm_activation = fuzz.interp_membership(rpm, aggregated, rpm_out)  # for plot




    # Visualize
    fig, (ax0, ax1, ax2,ax3) = plt.subplots(nrows=4, figsize=(8, 9))

    ax0.plot(volt, i_null, 'b', linewidth=1.5, )
    ax0.plot(volt, i_zero, 'r', linewidth=1.5, )
    ax0.plot(volt, i_small, 'b', linewidth=1.5, )
    ax0.plot(volt, i_medium, 'r', linewidth=1.5, )
    ax0.plot(volt, i_large, 'b', linewidth=1.5, )
    ax0.plot(volt, i_very_large, 'r', linewidth=1.5, )
    ax0.set_title('INPUT membership function (Volt)')
    ax0.legend()


    ax1.plot(rpm, o_zero, 'r', linewidth=1.5, )
    ax1.plot(rpm, o_small, 'b', linewidth=1.5, )
    ax1.plot(rpm, o_medium, 'r', linewidth=1.5, )
    ax1.plot(rpm, o_large, 'b', linewidth=1.5, )
    ax1.plot(rpm, o_very_large, 'r', linewidth=1.5, )
    ax1.set_title('OUTPUT membership function (RPM)')
    ax1.legend()

    ax2.fill_between(rpm, rmp_dummy, rpm_activation_zero, facecolor='b', alpha=0.7)
    ax2.plot(rpm, rpm_activation_zero, 'b', linewidth=0.5, linestyle='--', )
    ax2.fill_between(rpm, rmp_dummy, rpm_activation_small, facecolor='g', alpha=0.7)
    ax2.plot(rpm, rpm_activation_small, 'g', linewidth=0.5, linestyle='--')
    ax2.fill_between(rpm, rmp_dummy, rpm_activation_medium, facecolor='r', alpha=0.7)
    ax2.plot(rpm, rpm_activation_medium, 'r', linewidth=0.5, linestyle='--')
    ax2.fill_between(rpm, rmp_dummy, rpm_activation_large, facecolor='r', alpha=0.7)
    ax2.plot(rpm, rpm_activation_large, 'r', linewidth=0.5, linestyle='--')
    ax2.fill_between(rpm, rmp_dummy, rpm_activation_very_large, facecolor='r', alpha=0.7)
    ax2.plot(rpm, rpm_activation_very_large, 'r', linewidth=0.5, linestyle='--')
    ax2.set_title('Output membership activity')
    ax1.legend()



    ax3.plot(rpm, o_zero, 'b', linewidth=0.5, linestyle='--', )
    ax3.plot(rpm, o_small, 'g', linewidth=0.5, linestyle='--')
    ax3.plot(rpm, o_medium, 'r', linewidth=0.5, linestyle='--')
    ax3.plot(rpm, o_large, 'y', linewidth=0.5, linestyle='--', )
    ax3.plot(rpm, o_very_large, 'v', linewidth=0.5, linestyle='--')

    ax3.fill_between(rpm, rmp_dummy, aggregated, facecolor='Orange', alpha=0.7)
    ax3.plot([rpm_out, rpm_out], [0, rpm_activation], 'k', linewidth=1.5, alpha=0.9)
    ax3.set_title('Aggregated membership and result (line)')
    ax3.legend()

    # Turn off top/right axes
    for ax in (ax0, ax1, ax2,ax3):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    plt.savefig('output/out.png')
    # cv2.imwrite('output/output.png',(cv2.resize(cv2.imread('output/out.png')),(300,400)))

    return rpm_out
    # plt.show()

# if __name__ == '__main__':
#     value = 1.5
#     out = motor_rmp(value)
#     print(out)

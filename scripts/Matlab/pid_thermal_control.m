clc;
clear;
close all;

% ==========================================================
% SIMULATION PARAMETERS
% ==========================================================

dt = 0.1;
time_steps = 400;

ambient_temperature = -5.0;
target_temperature = 2.0;

thermal_capacity = 8.0;
heat_loss = 0.08;

% ==========================================================
% PID PARAMETERS
% ==========================================================

Kp = 2.5;
Ki = 0.12;
Kd = 0.8;

% ==========================================================
% INITIAL CONDITIONS
% ==========================================================

temperature_pid = 0.0;
temperature_onoff = 0.0;

integral = 0.0;
previous_error = 0.0;

% ==========================================================
% STORAGE
% ==========================================================

time_axis = zeros(time_steps, 1);

pid_response = zeros(time_steps, 1);
onoff_response = zeros(time_steps, 1);

% ==========================================================
% SIMULATION LOOP
% ==========================================================

for step = 1:time_steps

    t = (step - 1) * dt;

    % ======================================================
    % ON/OFF CONTROLLER
    % ======================================================

    if temperature_onoff < target_temperature
        heating_onoff = 1.2;
    else
        heating_onoff = 0.0;
    end

    dT_onoff = (
        heating_onoff 
        - heat_loss * (temperature_onoff - ambient_temperature)
    ) / thermal_capacity;

    temperature_onoff = temperature_onoff + dt * dT_onoff;

    % ======================================================
    % PID CONTROLLER
    % ======================================================

    error = target_temperature - temperature_pid;

    integral = integral + error * dt;

    derivative = (error - previous_error) / dt;

    control_signal = 
        Kp * error + 
        Ki * integral + 
        Kd * derivative;

    % Saturation limits
    control_signal = max(0.0, min(control_signal, 5.0));

    dT_pid = (
        control_signal 
        - heat_loss * (temperature_pid - ambient_temperature)
    ) / thermal_capacity;

    temperature_pid = temperature_pid + dt * dT_pid;

    previous_error = error;

    % ======================================================
    % STORE DATA
    % ======================================================

    time_axis(step) = t;

    pid_response(step) = temperature_pid;
    onoff_response(step) = temperature_onoff;

end

% ==========================================================
% PLOT
% ==========================================================

figure;

plot(time_axis, onoff_response, 
    'LineWidth', 2);
hold on;

plot(time_axis, pid_response, 
    'LineWidth', 2);

yline(target_temperature, '--');

xlabel('Time (s)');
ylabel('Temperature (°C)');

title('Controller Comparison');

legend( 
    'ON/OFF Control', 
    'PID Control', 
    'Target Temperature' 
);

grid on;

saveas(gcf, 'controller_comparison.png');
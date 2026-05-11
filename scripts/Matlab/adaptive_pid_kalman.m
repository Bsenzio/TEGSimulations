clc;
clear;
close all;

% ==========================================================
% SIMULATION PARAMETERS
% ==========================================================

dt = 0.1;
time_steps = 1500;

ambient_temperature = -5.0;
target_temperature = 2.0;

thermal_capacity = 8.0;
heat_loss = 0.06;

% ==========================================================
% PID PARAMETERS
% ==========================================================

% Classical PID
Kp = 2.5;
Ki = 0.12;
Kd = 0.55;

% Adaptive PID
Kp_adaptive = 2.2;
Ki_adaptive = 0.09;
Kd_adaptive = 0.65;

% ==========================================================
% INITIAL CONDITIONS
% ==========================================================

temperature_pid = 0.0;
temperature_adaptive = 0.0;

integral_pid = 0.0;
integral_adaptive = 0.0;

previous_error_pid = 0.0;
previous_error_adaptive = 0.0;

% ==========================================================
% KALMAN FILTER PARAMETERS
% ==========================================================

estimated_temperature = 0.0;

P = 1.0;
Q = 0.005;
R = 0.05;

% ==========================================================
% STORAGE
% ==========================================================

time_axis = zeros(time_steps,1);

pid_response = zeros(time_steps,1);
adaptive_response = zeros(time_steps,1);

measured_signal = zeros(time_steps,1);
estimated_signal = zeros(time_steps,1);

% ==========================================================
% SIMULATION LOOP
% ==========================================================

for step = 1:time_steps

    t = (step - 1) * dt;

    % ======================================================
    % ENVIRONMENTAL DISTURBANCE
    % ======================================================

    wind_disturbance = 0.18 * sin(0.10 * t);

    thermal_noise = normrnd(0, 0.025);

    % ======================================================
    % CLASSICAL PID
    % ======================================================

    error_pid = target_temperature - temperature_pid;

    integral_pid = integral_pid + error_pid * dt;

    integral_pid = max(-8, min(integral_pid, 8));

    derivative_pid = ...
        (error_pid - previous_error_pid) / dt;

    control_pid = ...
        Kp * error_pid + ...
        Ki * integral_pid + ...
        Kd * derivative_pid;

    control_pid = max(0, min(control_pid, 4.0));

    dT_pid = (
        control_pid ...
        - heat_loss * ...
        (temperature_pid - ambient_temperature) ...
        - wind_disturbance
    ) / thermal_capacity;

    temperature_pid = ...
        temperature_pid + dt * dT_pid;

    previous_error_pid = error_pid;

    % ======================================================
    % SENSOR MEASUREMENT
    % ======================================================

    measured_temp = ...
        temperature_adaptive + thermal_noise;

    % ======================================================
    % KALMAN FILTER
    % ======================================================

    predicted_temperature = estimated_temperature;

    P = P + Q;

    K = P / (P + R);

    estimated_temperature = ...
        predicted_temperature + ...
        K * (measured_temp - predicted_temperature);

    P = (1 - K) * P;

    % ======================================================
    % ADAPTIVE PID
    % ======================================================

    adaptive_gain = ...
        1.0 + ...
        abs(target_temperature - estimated_temperature) ...
        * 0.04;

    Kp_current = ...
        Kp_adaptive * adaptive_gain;

    Ki_current = Ki_adaptive;
    Kd_current = Kd_adaptive;

    error_adaptive = ...
        target_temperature - estimated_temperature;

    integral_adaptive = ...
        integral_adaptive + error_adaptive * dt;

    integral_adaptive = ...
        max(-8, min(integral_adaptive, 8));

    derivative_adaptive = ...
        (error_adaptive - previous_error_adaptive) / dt;

    control_adaptive = ...
        Kp_current * error_adaptive + ...
        Ki_current * integral_adaptive + ...
        Kd_current * derivative_adaptive;

    control_adaptive = ...
        max(0, min(control_adaptive, 4.0));

    dT_adaptive = (
        control_adaptive ...
        - heat_loss * ...
        (temperature_adaptive - ambient_temperature) ...
        - wind_disturbance
    ) / thermal_capacity;

    temperature_adaptive = ...
        temperature_adaptive + dt * dT_adaptive;

    previous_error_adaptive = error_adaptive;

    % ======================================================
    % STORE DATA
    % ======================================================

    time_axis(step) = t;

    pid_response(step) = temperature_pid;

    adaptive_response(step) = ...
        temperature_adaptive;

    measured_signal(step) = measured_temp;

    estimated_signal(step) = ...
        estimated_temperature;

end

% ==========================================================
% CONTROLLER COMPARISON
% ==========================================================

figure;

plot(time_axis, pid_response, ...
    'LineWidth', 2);
hold on;

plot(time_axis, adaptive_response, ...
    'LineWidth', 2);

yline(target_temperature, '--');

% Y AXIS EVERY 0.1°C
yticks(0:0.1:2.2);

ylim([0 2.2]);

xlabel('Time (s)');
ylabel('Temperature (°C)');

title('Adaptive PID vs Classical PID');

legend( ...
    'Classical PID', ...
    'Adaptive PID + Kalman', ...
    'Target Temperature' ...
);

grid on;

saveas(gcf, 'adaptive_pid_vs_pid.png');

% ==========================================================
% KALMAN ESTIMATION
% ==========================================================

figure;

plot(time_axis, measured_signal, ...
    'DisplayName', 'Noisy Measurement');
hold on;

plot(time_axis, estimated_signal, ...
    'LineWidth', 2, ...
    'DisplayName', 'Kalman Estimation');

% Y AXIS EVERY 0.1°C
yticks(-0.2:0.1:2.2);

ylim([-0.2 2.2]);

xlabel('Time (s)');
ylabel('Temperature (°C)');

title('Kalman Thermal State Estimation');

legend;

grid on;

saveas(gcf, 'kalman_estimation.png');
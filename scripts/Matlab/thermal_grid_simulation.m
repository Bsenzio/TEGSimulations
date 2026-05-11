clc;
clear;
close all;

% ==========================================================
% GRID PARAMETERS
% ==========================================================

GRID_SIZE = 10;

dt = 0.1;
time_steps = 400;

ambient_temperature = -5.0;

thermal_diffusion = 0.15;
heat_loss = 0.02;

target_temperature = 2.0;

% ==========================================================
% INITIAL TEMPERATURE GRID
% ==========================================================

T = ones(GRID_SIZE, GRID_SIZE) * ambient_temperature;

% Central heated area
for i = 4:7
    for j = 4:7
        T(i, j) = 0.0;
    end
end

% ==========================================================
% STORE HISTORY
% ==========================================================

history = zeros(GRID_SIZE, GRID_SIZE, time_steps);

% ==========================================================
% SIMULATION LOOP
% ==========================================================

for step = 1:time_steps

    T_new = T;

    for i = 1:GRID_SIZE
        for j = 1:GRID_SIZE

            center = T(i, j);

            % Boundary conditions
            if i > 1
                up = T(i - 1, j);
            else
                up = center;
            end

            if i < GRID_SIZE
                down = T(i + 1, j);
            else
                down = center;
            end

            if j > 1
                left = T(i, j - 1);
            else
                left = center;
            end

            if j < GRID_SIZE
                right = T(i, j + 1);
            else
                right = center;
            end

            % Laplacian
            laplacian = up + down + left + right - 4 * center;

            % Diffusion term
            diffusion_term = thermal_diffusion * laplacian;

            % Local heating model
            if center < target_temperature
                heating_term = 0.8;
            else
                heating_term = 0.0;
            end

            % Heat loss
            loss_term = heat_loss * (center - ambient_temperature);

            % Temperature update
            dT = diffusion_term + heating_term - loss_term;

            T_new(i, j) = center + dt * dT;

        end
    end

    T = T_new;

    history(:, :, step) = T;

end

% ==========================================================
% FINAL THERMAL MAP
% ==========================================================

figure;

imagesc(T);

colormap('hot');
colorbar;

axis equal tight;

title('Thermal Rooftop Distribution');

xlabel('Node X');
ylabel('Node Y');

saveas(gcf, 'thermal_map.png');

% ==========================================================
% TRANSIENT RESPONSE
% ==========================================================

center_temperature = zeros(time_steps, 1);

for k = 1:time_steps
    center_temperature(k) = history(6, 6, k);
end

time_axis = (0:time_steps-1) * dt;

figure;

plot(time_axis, center_temperature, 'LineWidth', 2);
hold on;

yline(target_temperature, '--');

xlabel('Time (s)');
ylabel('Temperature (°C)');

title('Transient Thermal Response');

grid on;

saveas(gcf, 'transient_response.png');
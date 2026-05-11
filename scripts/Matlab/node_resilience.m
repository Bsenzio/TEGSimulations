clc;
clear;
close all;

% -----------------------------------
% PARAMETERS
% -----------------------------------

GRID_SIZE = 30;
TIME_STEPS = 150;

ambient_temp = -6.0;
target_temp = 1.0;

diffusion = 0.18;
heating_power = 0.30;

% Failure parameters
failure_ratio = 0.20;

% -----------------------------------
% INITIAL GRID
% -----------------------------------

temperature = ones(GRID_SIZE, GRID_SIZE) * ambient_temp;

% Central heating region
for i = 11:20
    for j = 11:20
        temperature(i, j) = 1.0;
    end
end

% -----------------------------------
% NODE FAILURE MAP
% -----------------------------------

failure_map = ones(GRID_SIZE, GRID_SIZE);

num_failures = round( ...
    GRID_SIZE * GRID_SIZE * failure_ratio);

failed_indices = randperm( ...
    GRID_SIZE * GRID_SIZE, ...
    num_failures);

for k = 1:length(failed_indices)

    idx = failed_indices(k);

    x = floor((idx - 1) / GRID_SIZE) + 1;
    y = mod((idx - 1), GRID_SIZE) + 1;

    failure_map(x, y) = 0;

end

% -----------------------------------
% STORAGE
% -----------------------------------

avg_temp_normal = zeros(TIME_STEPS,1);
avg_temp_failure = zeros(TIME_STEPS,1);

% -----------------------------------
% NORMAL OPERATION
% -----------------------------------

temp_normal = temperature;

for t = 1:TIME_STEPS

    new_temp = temp_normal;

    for i = 2:GRID_SIZE-1
        for j = 2:GRID_SIZE-1

            laplacian = ...
                temp_normal(i+1, j) + ...
                temp_normal(i-1, j) + ...
                temp_normal(i, j+1) + ...
                temp_normal(i, j-1) - ...
                4 * temp_normal(i, j);

            control = ...
                heating_power * ...
                (target_temp - temp_normal(i, j));

            new_temp(i, j) = ...
                new_temp(i, j) + ...
                diffusion * laplacian + ...
                0.05 * control;

        end
    end

    temp_normal = new_temp;

    avg_temp_normal(t) = ...
        mean(temp_normal(:));

end

% -----------------------------------
% FAILURE + ADAPTIVE RECOVERY
% -----------------------------------

temp_failure = temperature;

for t = 1:TIME_STEPS

    new_temp = temp_failure;

    for i = 2:GRID_SIZE-1
        for j = 2:GRID_SIZE-1

            laplacian = ...
                temp_failure(i+1, j) + ...
                temp_failure(i-1, j) + ...
                temp_failure(i, j+1) + ...
                temp_failure(i, j-1) - ...
                4 * temp_failure(i, j);

            % Failed node
            if failure_map(i, j) == 0

                control = -0.08;

            else

                % Neighbor-aware adaptive recovery
                nearby_failures = ...
                    (failure_map(i+1, j) == 0) || ...
                    (failure_map(i-1, j) == 0) || ...
                    (failure_map(i, j+1) == 0) || ...
                    (failure_map(i, j-1) == 0);

                if nearby_failures
                    adaptive_gain = 1.1;
                else
                    adaptive_gain = 1.0;
                end

                control = ...
                    adaptive_gain * ...
                    heating_power * ...
                    (target_temp - temp_failure(i, j));

            end

            new_temp(i, j) = ...
                new_temp(i, j) + ...
                diffusion * laplacian + ...
                0.05 * control;

        end
    end

    temp_failure = new_temp;

    avg_temp_failure(t) = ...
        mean(temp_failure(:));

end

% -----------------------------------
% THERMAL MAPS
% -----------------------------------

figure('Position', [100 100 1400 400]);

% Normal thermal distribution
subplot(1,3,1);

imagesc(temp_normal);

colormap('hot');
caxis([-6 1.5]);

title('Normal Distribution', ...
    'FontSize', 10);

axis off;

% Failure map
subplot(1,3,2);

imagesc(failure_map);

colormap('gray');

title('Failure Map', ...
    'FontSize', 10);

axis off;

% Adaptive recovery distribution
subplot(1,3,3);

imagesc(temp_failure);

colormap('hot');
caxis([-6 1.5]);

title('Adaptive Recovery', ...
    'FontSize', 10);

axis off;

% Shared colorbar
colorbar;

saveas(gcf, ...
    'fault_tolerant_thermal_maps.png');

% -----------------------------------
% STABILITY RESPONSE
% -----------------------------------

figure;

plot(avg_temp_normal, ...
    'LineWidth', 2);
hold on;

plot(avg_temp_failure, ...
    'LineWidth', 2);

yline(target_temp, '--');

xlabel('Time Step');
ylabel('Average Temperature (°C)');

title( ...
    'Fault-Tolerant Thermal Regulation', ...
    'FontSize', 11);

legend( ...
    'Normal Operation', ...
    'Failure + Recovery', ...
    'Target Temperature', ...
    'FontSize', 8);

grid on;

saveas(gcf, ...
    'fault_tolerant_response.png');
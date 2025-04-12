def get_state(entity_id):
    return hass.states.get(entity_id).state

def calculate_inner_color(house_power_value):
    if 300 <= house_power_value < 1000:
        return (0, 128, 0)  # Green
    elif 1000 <= house_power_value < 2000:
        return (128, 128, 0)  # Yellow
    elif house_power_value >= 2000:
        return (128, 0, 0)  # Red
    return (0, 0, 128)  # Default Blue

def price_to_color(slot_price_value):
    if slot_price_value < 0:
        return (0, 0, 128)  # Blue
    elif slot_price_value > 200:
        return (128, 0, 0)  # Red
    elif slot_price_value <= 100:
        # Green to Yellow: increase red from 0 to 128
        red_value = int((slot_price_value / 100) * 128)
        green_value = 128
    else:
        # Yellow to Red: decrease green from 128 to 0
        red_value = 128
        green_value = int(((200 - slot_price_value) / 100) * 128)
    return (red_value, green_value, 0)

def build_inner_ring(soc_value, soc_minimum, diode_count=24):
    lit_count = int(round((soc_value - soc_minimum) / ((100 - soc_minimum) / diode_count), 0))
    return list(range(lit_count)) if lit_count > 0 else [diode_count - 1]

def apply_price_colors(diodes_array, price_list, ref_hour, ref_quarter, is_today_data=True):
    for price_hour, price_value in price_list:
        if is_today_data and price_hour < ref_hour:
            continue
        if not is_today_data and price_hour > ref_hour:
            break

        for quarter_index in range(4):
            diode_index = price_hour * 4 + quarter_index
            if is_today_data and price_hour == ref_hour and quarter_index < ref_quarter:
                continue
            if not is_today_data and price_hour == ref_hour and quarter_index >= ref_quarter:
                continue

            effect_mode = 'pulsing' if (price_hour == ref_hour and quarter_index == ref_quarter) else 'solid'
            diodes_array[diode_index] = (price_to_color(price_value), effect_mode)

# --- Fetch sensor data ---
battery_soc = float(get_state('sensor.pixel_8_battery_level_2'))
purchased_power = float(get_state('sensor.aktiv_effekt_uttag_momentan_trefaseffekt'))
sold_power = float(get_state('sensor.aktiv_effekt_inmatning_momentan_trefaseffekt'))
solar_battery_power = 0

# --- Calculate power flows ---
grid_power = (purchased_power - sold_power) * 1000
house_power = grid_power - solar_battery_power
minimum_soc = 0

# --- Inner ring color & diode setup ---
inner_color = calculate_inner_color(house_power)
inner_diodes = build_inner_ring(battery_soc, minimum_soc)

# --- Time info & Nordpool data ---
nordpool_state = hass.states.get("sensor.nordpool_kwh_se3_sek_3_10_025")
nordpool_attributes = nordpool_state.attributes
now = dt_util.now()
current_hour = now.hour
current_quarter = now.minute // 15
price_today = list(enumerate(nordpool_attributes.get('today')))
price_tomorrow = list(enumerate(nordpool_attributes.get('tomorrow')))
tomorrow_valid = nordpool_attributes.get('tomorrow_valid')

# --- Initialize LED state ---
diodes_state = [((0, 0, 0), 'solid')] * 120

# --- Apply price-based colors ---
apply_price_colors(diodes_state, price_today, current_hour, current_quarter, is_today_data=True)
apply_price_colors(diodes_state, price_tomorrow, current_hour, current_quarter, is_today_data=False)

# --- Set inner ring LEDs ---
inner_ring_offset = 96
for diode_id in inner_diodes:
    diodes_state[diode_id + inner_ring_offset] = (inner_color, 'solid')

# --- Final output ---
output['data'] = diodes_state
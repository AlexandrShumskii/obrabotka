import pandas as pd
import my_plot as mp

file = "household_power_consumption.txt"

df = pd.read_csv(
    file,
    sep = ';',
    skiprows=0,
    dtype=str,
    encoding="cp1251"
)
df['Date and Time'] = pd.to_datetime(
    df['Date'] + ' ' + df['Time'],
    format='%d/%m/%Y %H:%M:%S'
)
cols = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3'
]

df[cols] = df[cols].apply(
    pd.to_numeric,
    errors='coerce'
)
df = df.dropna(subset=['Date and Time'])
df['Hour'] = df['Date and Time'].dt.hour
daily_profile = df.groupby('Hour')[
    'Global_active_power'
].mean()

mp.plot_single(daily_profile.index,daily_profile.values, xlabel = 'время суток', ylabel = 'активная мощность потребления', title = 'средний суточный профиль потребления')
# часть 2. зависимость от полноты
# Количество измерений за каждый день
daily_counts = df.groupby(
    df['Date and Time'].dt.date
)['Global_active_power'].count()

# Полнота данных в процентах
daily_completeness = daily_counts / 1440 * 100

print(daily_completeness.describe())

print('Средняя полнота:',
      daily_completeness.mean(), '%')
print('Дней с полнотой >= 95%:',
      (daily_completeness >= 95).sum())

print('Дней с полнотой >= 80%:',
      (daily_completeness >= 80).sum())

print('Дней с полнотой < 50%:',
      (daily_completeness < 50).sum())
df['Day'] = df['Date and Time'].dt.date

completeness = (
    df.groupby('Day')['Global_active_power']
    .count() / 1440
)
# Дни с полнотой >= 95%
good_days = completeness[completeness >= 0.95].index

profile_95 = df[df['Day'].isin(good_days)].groupby(
    'Hour'
)['Global_active_power'].mean()

# Дни с полнотой >= 80%
medium_days = completeness[completeness >= 0.80].index

profile_80 = df[df['Day'].isin(medium_days)].groupby(
    'Hour'
)['Global_active_power'].mean()

items = [{'x': profile_95.index, 'y': profile_95.values, 'xlabel': 'часы', 'ylabel': 'потребление', 'title': 'дни с полнотой более 95%', 'color':'blue', 'label':''},
         {'x': profile_80.index, 'y': profile_80.values, 'xlabel': 'часы', 'ylabel': 'потребление', 'title': 'дни с полнотой более 80%','color':'red', 'label':''}]
mp.plot_grid(1,2, items = items, suptitle = 'зависимость от полноты данных')
# часть 3 зависимость от способа обработки

# Среднее арифметическое по всем измерениям
mean_profile = df.groupby('Hour')[
    'Global_active_power'
].mean()

# Медиана по всем измерениям
median_profile = df.groupby('Hour')[
    'Global_active_power'
].median()

# Сначала считаем среднее для каждого часа каждого дня
hourly_by_day = df.groupby(
    ['Day', 'Hour']
)['Global_active_power'].mean()

# Затем усредняем полученные профили по дням
equal_day_profile = hourly_by_day.groupby(
    'Hour'
).mean()
items2 = [{'x':mean_profile.index, 'y':mean_profile.values, 'xtitle': 'часы', 'ytitle': 'потребление', 'title': 'усреднённое по всем значениям','color':'blue', 'label':'',},
           {'x':median_profile.index, 'y':median_profile.values, 'xtitle': 'часы', 'ytitle': 'потребление', 'title': 'медианное','color':'red','label':''},
           {'x':equal_day_profile.index, 'y':equal_day_profile.values, 'xtitle': 'часы', 'ytitle': 'потребление', 'title': 'усреднённое по дням','color':'green','label':''}]
mp.plot_grid(1,3,items = items2, suptitle = 'зависимость от способа обработки данных', figsize = (12,5))
print('Вывод: 1) полнота данных практически никак не влияет на результат ',
      '2) способ обработки влияет: медианное сильно отличается от усреднённых, а усреднённые по всем значениям и по дням почти не отличаются')
import pandas as pd
from tabulate import tabulate

chord_name = None
chord_root = None
chord_span = None
chord_lower_pole = None
chord_upper_pole = None
chord_mass_center = ['C', 'D']

tension_note = ['F']
tension_position = None
tension_type = ['T0', 'T1', 'T2']
span_range = (5, 7)

df = pd.read_csv('diatonic_tensions.csv', sep=',')
df_filtered = df[(df.chord_mass_center.isin(chord_mass_center)) & (df.tension_note.isin(tension_note)) & df.tension_type.isin(tension_type) & (df.new_span.isin(range(*span_range)))]

print(tabulate(df_filtered, headers='keys', tablefmt='psql'))

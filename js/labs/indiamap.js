/* Knowtopia Concept Lab: indiamap — stylised map of India (official outline incl. all of
   Jammu & Kashmir and Ladakh, Andaman & Nicobar and Lakshadweep).

   PARAMS (all optional — missing ones fall back to `example`)
   ─────────────────────────────────────────────────────────────────────────────────────────
   title       string   Heading above the map.                                 'India map'
   mode        string   Starting mode: 'explore' | 'find' | 'latitude'.         'explore'
   modes       string[] Mode tabs to show (one entry = no tabs).               [mode]
   challenge   string   Challenge text for the starting mode (else generated).
   places      object[] Points: {name, lat, lon, emoji?, info?}               (example cities)
   lines       object[] Polylines e.g. rivers: {name, pts:[[lon,lat],…], color?, info?}   []
   regions     object[] Shaded areas: {name, pts:[[lon,lat],…], color?, info?}            []
   goal        number   explore: how many different items to tap to win.     min(5, items)
   ask         string[] find: names to ask (places / lines / regions).       all places
   rounds      number   find: correct answers needed to win.                 min(4, ask)
   radius      number   find: accept a tap within this many km of a place.   150
   grid        boolean  Draw latitude/longitude grid every 5°.               true in 'latitude'
   tropic      boolean  Draw Tropic of Cancer (23.5° N).                     true
   meridian    boolean  Draw Standard Meridian (82.5° E, IST).               true
   target      object   latitude: {lat?, lon?, tol?(deg, default 0.8)} — drag the pin here.
                        Default: where the Tropic of Cancer meets 82.5° E.
   labels      boolean  Show place names on the map in explore mode.         true

   What the child does: explore = tap places/rivers/regions to learn (and see the direction &
   distance from the previous place); find = tap where the asked place is (direction hints on a
   miss); latitude = drag a pin and read latitude, longitude, Tropic side and local sun time vs IST.
*/
(function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  /* India boundary: DataMeet "india-composite" (Survey of India official outline incl. J&K and Ladakh), CC-0, simplified. */
  const MAIN = [[77.52, 35.49], [77.91, 35.46], [77.94, 35.56], [78.16, 35.55], [78.24, 35.73], [78.8, 35.87], [78.86, 35.97], [79.03, 35.91], [79.34, 35.99], [79.49, 35.85], [79.57, 35.9], [79.7, 35.64], [80.0, 35.6], [80.05, 35.42], [80.21, 35.58], [80.41, 35.48], [80.29, 35.35], [80.21, 34.89], [80.07, 34.71], [79.79, 34.63], [79.79, 34.48], [79.51, 34.45], [79.61, 34.24], [79.4, 34.0], [78.89, 33.97], [79.09, 33.64], [78.91, 33.62], [78.94, 33.38], [79.11, 33.2], [79.41, 33.19], [79.33, 33.0], [79.55, 32.68], [79.41, 32.52], [79.28, 32.56], [78.97, 32.34], [78.78, 32.48], [78.74, 32.7], [78.4, 32.53], [78.49, 32.28], [78.78, 31.99], [78.7, 31.81], [78.85, 31.61], [78.72, 31.51], [78.78, 31.31], [78.9, 31.29], [79.1, 31.45], [79.43, 31.02], [79.6, 30.94], [79.87, 30.97], [80.24, 30.76], [80.22, 30.58], [81.03, 30.25], [80.37, 29.75], [80.41, 29.6], [80.24, 29.44], [80.3, 29.21], [80.14, 29.1], [80.08, 28.82], [80.52, 28.55], [80.57, 28.69], [81.21, 28.36], [81.32, 28.13], [81.45, 28.16], [81.88, 27.86], [82.07, 27.92], [82.45, 27.68], [82.71, 27.72], [82.74, 27.5], [83.19, 27.45], [83.32, 27.33], [83.39, 27.48], [83.86, 27.35], [83.85, 27.45], [84.15, 27.52], [84.29, 27.39], [84.62, 27.34], [84.64, 27.05], [84.96, 26.96], [85.02, 26.85], [85.19, 26.87], [85.21, 26.76], [85.63, 26.87], [85.85, 26.57], [86.03, 26.67], [86.33, 26.62], [86.73, 26.42], [87.07, 26.59], [87.09, 26.45], [87.34, 26.35], [87.89, 26.49], [88.01, 26.36], [88.19, 26.74], [88.14, 26.99], [87.99, 27.12], [88.2, 27.79], [88.12, 27.92], [88.64, 28.12], [88.84, 28.02], [88.89, 27.86], [88.76, 27.57], [88.91, 27.29], [88.75, 27.14], [88.87, 27.11], [88.88, 26.94], [88.92, 26.99], [89.13, 26.81], [89.38, 26.86], [89.86, 26.7], [90.36, 26.9], [90.72, 26.77], [91.69, 26.81], [91.89, 26.92], [92.06, 26.85], [92.12, 26.96], [92.04, 27.26], [92.12, 27.29], [92.02, 27.48], [91.65, 27.48], [91.56, 27.63], [91.64, 27.76], [91.92, 27.72], [92.24, 27.89], [92.46, 27.79], [92.73, 27.98], [92.68, 28.15], [92.92, 28.2], [93.43, 28.66], [93.71, 28.66], [94.26, 28.93], [94.37, 29.03], [94.29, 29.15], [94.63, 29.3], [94.81, 29.16], [95.26, 29.07], [96.05, 29.38], [96.3, 29.19], [96.19, 29.04], [96.33, 29.11], [96.63, 28.73], [96.41, 28.51], [96.5, 28.43], [96.49, 28.54], [96.71, 28.61], [96.93, 28.35], [97.13, 28.36], [97.36, 28.2], [97.31, 28.06], [97.4, 28.01], [97.37, 27.88], [97.25, 27.9], [96.89, 27.61], [97.14, 27.09], [96.87, 27.18], [96.88, 27.26], [96.7, 27.37], [96.23, 27.28], [95.43, 26.7], [95.15, 26.62], [95.06, 26.45], [95.19, 26.07], [95.01, 25.9], [95.05, 25.76], [94.9, 25.57], [94.63, 25.4], [94.58, 25.21], [94.74, 25.13], [94.71, 24.94], [94.4, 24.48], [94.16, 23.85], [93.75, 24.01], [93.51, 23.94], [93.33, 24.08], [93.44, 23.69], [93.39, 23.13], [93.29, 23.01], [93.13, 23.04], [93.11, 22.53], [93.2, 22.26], [93.15, 22.18], [93.04, 22.2], [93.01, 21.99], [92.95, 22.03], [92.91, 21.94], [92.7, 22.16], [92.6, 21.98], [92.28, 23.72], [92.05, 23.65], [91.96, 23.73], [91.97, 23.48], [91.76, 23.3], [91.84, 23.09], [91.62, 22.94], [91.45, 23.26], [91.38, 23.21], [91.42, 23.06], [91.35, 23.1], [91.32, 23.36], [91.16, 23.61], [91.37, 24.11], [91.59, 24.07], [91.67, 24.23], [91.76, 24.14], [91.74, 24.25], [91.9, 24.14], [91.92, 24.34], [92.16, 24.42], [92.3, 24.74], [92.23, 24.9], [92.5, 24.88], [92.43, 25.03], [92.06, 25.19], [90.44, 25.14], [89.84, 25.29], [89.82, 25.82], [89.89, 25.95], [89.68, 26.24], [89.58, 25.97], [89.36, 26.01], [89.16, 26.14], [89.09, 26.4], [88.9, 26.41], [89.05, 26.24], [88.67, 26.26], [88.75, 26.35], [88.4, 26.63], [88.33, 26.48], [88.49, 26.46], [88.52, 26.36], [88.18, 26.15], [88.11, 25.82], [88.27, 25.81], [88.54, 25.51], [88.81, 25.52], [88.84, 25.36], [89.01, 25.26], [88.92, 25.17], [88.44, 25.21], [88.4, 24.95], [88.33, 24.87], [88.14, 24.94], [88.18, 24.86], [88.01, 24.67], [88.33, 24.38], [88.74, 24.28], [88.77, 23.98], [88.58, 23.86], [88.56, 23.65], [88.8, 23.5], [88.72, 23.26], [89.0, 23.22], [88.84, 23.01], [88.97, 22.84], [88.94, 22.56], [89.1, 22.16], [88.99, 21.9], [89.1, 21.64], [88.92, 21.63], [88.86, 21.78], [88.85, 21.62], [88.72, 21.68], [88.78, 22.01], [88.64, 22.08], [88.55, 21.82], [88.52, 21.95], [88.46, 21.9], [88.45, 21.61], [88.42, 21.72], [88.4, 21.59], [88.4, 21.72], [88.27, 21.73], [88.25, 21.56], [88.16, 21.96], [88.21, 22.15], [88.02, 22.22], [88.19, 22.1], [87.8, 21.7], [87.09, 21.54], [86.91, 21.34], [86.83, 21.14], [86.97, 20.82], [86.87, 20.78], [87.07, 20.72], [86.73, 20.53], [86.71, 20.41], [86.79, 20.38], [86.67, 20.29], [86.8, 20.35], [86.52, 20.18], [86.42, 20.0], [86.32, 19.99], [86.37, 19.95], [85.54, 19.7], [85.04, 19.39], [84.13, 18.31], [83.56, 18.03], [83.21, 17.59], [82.31, 17.04], [82.25, 16.88], [82.36, 16.82], [82.33, 16.99], [82.37, 16.91], [82.27, 16.71], [82.37, 16.71], [82.31, 16.6], [82.26, 16.69], [82.3, 16.56], [81.71, 16.31], [81.55, 16.37], [81.27, 16.29], [80.94, 15.71], [80.83, 15.7], [80.81, 15.84], [80.68, 15.89], [80.26, 15.67], [80.05, 15.07], [80.2, 14.58], [80.13, 14.07], [80.35, 13.28], [80.16, 12.46], [79.87, 12.04], [79.76, 11.67], [79.88, 10.31], [79.64, 10.37], [79.29, 10.26], [79.27, 10.04], [78.9, 9.49], [78.96, 9.34], [79.19, 9.28], [78.86, 9.25], [78.27, 9.02], [78.07, 8.37], [77.55, 8.07], [77.32, 8.12], [77.01, 8.35], [76.55, 8.9], [76.67, 8.99], [76.54, 8.93], [76.36, 9.36], [76.27, 10.03], [76.22, 10.0], [76.21, 10.2], [75.91, 10.78], [75.87, 11.12], [75.54, 11.71], [75.2, 12.0], [74.83, 12.84], [74.7, 13.34], [74.72, 13.64], [74.43, 14.27], [74.52, 14.24], [74.42, 14.29], [74.28, 14.71], [74.12, 14.77], [74.16, 14.86], [73.91, 15.08], [73.9, 15.33], [73.78, 15.41], [73.89, 15.43], [73.73, 15.59], [73.79, 15.65], [73.73, 15.61], [73.46, 16.05], [73.37, 16.38], [73.47, 16.41], [73.37, 16.39], [73.32, 16.51], [73.44, 16.5], [73.32, 16.6], [73.4, 16.62], [73.31, 16.73], [73.33, 16.97], [73.26, 17.05], [73.33, 17.04], [73.19, 17.3], [73.3, 17.29], [73.17, 17.4], [73.14, 17.56], [73.22, 17.59], [73.14, 17.61], [73.03, 17.95], [73.09, 17.99], [72.93, 18.22], [72.97, 18.28], [73.1, 18.14], [73.09, 18.32], [73.03, 18.26], [72.92, 18.35], [72.91, 18.54], [73.01, 18.47], [72.86, 18.69], [72.94, 18.83], [73.02, 18.72], [72.91, 18.9], [73.07, 19.02], [73.0, 19.0], [72.99, 19.19], [72.81, 18.89], [72.79, 19.3], [72.91, 19.29], [72.74, 19.46], [72.89, 19.52], [72.73, 19.53], [72.66, 19.83], [72.9, 20.53], [72.85, 20.74], [72.93, 20.76], [72.83, 20.79], [72.85, 20.97], [72.76, 20.93], [72.73, 21.0], [72.85, 21.03], [72.71, 21.09], [72.79, 21.18], [72.64, 21.08], [72.64, 21.21], [72.74, 21.2], [72.6, 21.3], [72.76, 21.45], [72.65, 21.45], [72.68, 21.5], [72.93, 21.68], [72.54, 21.66], [72.62, 21.91], [72.75, 21.97], [72.54, 21.9], [72.51, 21.98], [72.59, 22.2], [72.76, 22.17], [72.91, 22.26], [72.54, 22.31], [72.43, 22.2], [72.33, 22.31], [72.3, 22.1], [72.18, 22.02], [72.25, 21.92], [72.16, 21.96], [72.31, 21.63], [72.09, 21.32], [72.11, 21.2], [71.44, 20.87], [70.82, 20.69], [70.16, 21.05], [68.94, 22.31], [69.07, 22.48], [69.04, 22.39], [69.19, 22.42], [69.23, 22.26], [69.48, 22.33], [69.51, 22.43], [69.67, 22.32], [69.73, 22.47], [69.81, 22.4], [69.99, 22.54], [70.17, 22.54], [70.45, 22.97], [70.29, 22.94], [70.22, 23.06], [70.22, 22.95], [69.88, 22.91], [69.71, 22.74], [69.45, 22.78], [69.36, 22.88], [69.2, 22.84], [68.63, 23.17], [68.72, 23.13], [68.58, 23.23], [68.68, 23.3], [68.45, 23.48], [68.47, 23.55], [68.43, 23.51], [68.55, 23.71], [68.81, 23.88], [68.51, 23.75], [68.43, 23.82], [68.35, 23.58], [68.17, 23.62], [68.35, 23.73], [68.19, 23.73], [68.36, 23.97], [68.75, 23.97], [68.81, 24.31], [68.87, 24.21], [68.95, 24.3], [69.0, 24.22], [69.59, 24.29], [69.73, 24.17], [70.03, 24.17], [70.11, 24.3], [70.56, 24.42], [70.57, 24.25], [70.71, 24.22], [71.12, 24.4], [71.0, 24.44], [70.99, 24.6], [71.1, 24.69], [70.89, 25.15], [70.66, 25.4], [70.66, 25.7], [70.27, 25.71], [70.1, 25.94], [70.17, 26.55], [69.82, 26.59], [69.51, 26.74], [69.59, 27.18], [70.37, 28.01], [70.59, 28.01], [70.74, 27.74], [70.87, 27.71], [71.9, 27.96], [72.39, 28.77], [72.95, 29.03], [73.28, 29.57], [73.4, 29.95], [73.97, 30.2], [73.88, 30.36], [73.93, 30.49], [74.07, 30.52], [74.42, 30.94], [74.7, 31.07], [74.51, 31.13], [74.55, 31.36], [74.65, 31.43], [74.49, 31.72], [74.61, 31.89], [74.88, 32.05], [75.24, 32.09], [75.37, 32.23], [75.1, 32.48], [74.68, 32.49], [74.71, 32.84], [74.64, 32.75], [74.37, 32.77], [73.93, 33.03], [73.63, 33.09], [73.59, 33.89], [73.4, 34.38], [73.45, 34.57], [73.66, 34.56], [73.73, 34.76], [74.05, 34.89], [74.13, 35.12], [73.75, 35.22], [73.69, 35.35], [73.79, 35.52], [73.41, 35.53], [73.33, 35.66], [73.13, 35.72], [73.18, 35.86], [72.57, 35.85], [72.55, 36.23], [72.97, 36.48], [73.06, 36.7], [73.85, 36.72], [73.67, 36.92], [74.04, 36.83], [74.42, 37.01], [74.56, 36.97], [74.69, 37.1], [74.84, 37.07], [74.9, 36.94], [75.15, 37.03], [75.42, 36.96], [75.46, 36.73], [75.74, 36.75], [76.03, 36.44], [76.72, 36.16], [76.84, 35.86], [77.35, 35.72], [77.52, 35.49]];
  const ISLANDS = [ /* Andaman & Nicobar */
    [[93.05, 13.55], [93.05, 13.48], [93.03, 13.46], [93.04, 13.43], [93.02, 13.43], [93.05, 13.4], [93.07, 13.41], [93.08, 13.4], [93.06, 13.38], [93.1, 13.33], [93.07, 13.31], [93.07, 13.32], [93.05, 13.32], [93.05, 13.35], [93.01, 13.35], [93.0, 13.32], [92.97, 13.36], [92.96, 13.34], [93.01, 13.31], [93.0, 13.29], [93.02, 13.32], [93.02, 13.27], [93.07, 13.26], [93.04, 13.19], [93.04, 13.06], [93.01, 13.02], [92.98, 13.03], [92.97, 13.01], [92.94, 13.03], [92.95, 13.1], [92.94, 13.05], [92.9, 13.09], [92.92, 13.06], [92.89, 13.04], [92.92, 13.04], [92.91, 13.0], [92.95, 12.97], [92.91, 12.94], [92.91, 12.99], [92.89, 12.94], [92.86, 12.94], [92.88, 12.88], [92.81, 12.9], [92.8, 12.97], [92.83, 12.98], [92.84, 13.01], [92.79, 13.01], [92.8, 13.09], [92.82, 13.07], [92.81, 13.09], [92.83, 13.11], [92.82, 13.12], [92.86, 13.14], [92.82, 13.15], [92.82, 13.17], [92.84, 13.17], [92.83, 13.18], [92.84, 13.23], [92.86, 13.24], [92.83, 13.27], [92.85, 13.3], [92.83, 13.31], [92.85, 13.37], [92.86, 13.36], [92.89, 13.39], [92.85, 13.4], [92.89, 13.4], [92.88, 13.47], [92.91, 13.48], [92.91, 13.5], [92.94, 13.49], [92.92, 13.5], [92.94, 13.52], [92.93, 13.53], [93.0, 13.53], [93.0, 13.57], [93.02, 13.54], [93.04, 13.57], [93.05, 13.55]],
    [[92.71, 12.23], [92.72, 12.19], [92.71, 12.16], [92.74, 12.18], [92.76, 12.17], [92.74, 12.1], [92.75, 12.05], [92.71, 12.05], [92.75, 12.06], [92.8, 12.05], [92.77, 12.02], [92.74, 12.03], [92.77, 12.0], [92.75, 11.99], [92.76, 11.98], [92.73, 11.98], [92.74, 11.96], [92.72, 11.96], [92.72, 11.92], [92.74, 11.89], [92.75, 11.93], [92.79, 11.94], [92.8, 11.9], [92.76, 11.7], [92.75, 11.7], [92.75, 11.68], [92.71, 11.7], [92.7, 11.69], [92.71, 11.69], [92.72, 11.67], [92.67, 11.65], [92.68, 11.62], [92.69, 11.63], [92.7, 11.62], [92.71, 11.65], [92.74, 11.65], [92.73, 11.68], [92.76, 11.66], [92.76, 11.64], [92.74, 11.63], [92.76, 11.63], [92.76, 11.61], [92.72, 11.47], [92.71, 11.5], [92.66, 11.51], [92.66, 11.57], [92.63, 11.56], [92.61, 11.61], [92.64, 11.61], [92.65, 11.63], [92.61, 11.63], [92.61, 11.71], [92.58, 11.71], [92.57, 11.69], [92.56, 11.84], [92.53, 11.82], [92.52, 11.84], [92.57, 11.94], [92.59, 11.88], [92.61, 11.89], [92.61, 11.85], [92.63, 12.1], [92.67, 12.21], [92.68, 12.17], [92.68, 12.21], [92.7, 12.24], [92.71, 12.23]],
    [[92.91, 12.91], [92.93, 12.91], [92.91, 12.88], [92.94, 12.88], [92.96, 12.84], [92.96, 12.79], [92.94, 12.77], [92.99, 12.71], [92.98, 12.7], [92.97, 12.62], [92.95, 12.62], [92.97, 12.61], [92.99, 12.53], [92.98, 12.49], [92.96, 12.49], [92.93, 12.46], [92.97, 12.46], [92.93, 12.44], [92.92, 12.4], [92.9, 12.44], [92.91, 12.46], [92.89, 12.44], [92.85, 12.47], [92.91, 12.42], [92.89, 12.41], [92.81, 12.44], [92.81, 12.46], [92.81, 12.43], [92.84, 12.42], [92.87, 12.36], [92.9, 12.35], [92.88, 12.33], [92.9, 12.32], [92.83, 12.3], [92.78, 12.32], [92.75, 12.3], [92.71, 12.33], [92.72, 12.6], [92.69, 12.61], [92.72, 12.61], [92.72, 12.64], [92.73, 12.62], [92.76, 12.67], [92.78, 12.67], [92.79, 12.63], [92.8, 12.7], [92.78, 12.67], [92.74, 12.67], [92.75, 12.72], [92.73, 12.82], [92.74, 12.83], [92.75, 12.81], [92.76, 12.84], [92.79, 12.82], [92.8, 12.89], [92.86, 12.89], [92.87, 12.88], [92.91, 12.91]],
    [[93.85, 7.24], [93.86, 7.21], [93.89, 7.2], [93.9, 7.09], [93.93, 7.03], [93.96, 7.0], [93.94, 7.01], [93.93, 7.0], [93.96, 6.96], [93.91, 6.91], [93.91, 6.85], [93.93, 6.84], [93.91, 6.81], [93.89, 6.79], [93.87, 6.82], [93.84, 6.75], [93.82, 6.76], [93.83, 6.82], [93.8, 6.84], [93.79, 6.88], [93.8, 6.88], [93.77, 6.92], [93.76, 6.91], [93.73, 6.99], [93.7, 7.02], [93.67, 7.02], [93.66, 7.1], [93.68, 7.12], [93.66, 7.13], [93.69, 7.16], [93.69, 7.19], [93.73, 7.19], [93.76, 7.22], [93.81, 7.21], [93.81, 7.24], [93.85, 7.24]],
    [[92.55, 10.88], [92.54, 10.87], [92.56, 10.86], [92.55, 10.88], [92.59, 10.85], [92.6, 10.79], [92.57, 10.8], [92.62, 10.76], [92.62, 10.67], [92.55, 10.59], [92.58, 10.57], [92.52, 10.51], [92.44, 10.54], [92.39, 10.53], [92.42, 10.63], [92.39, 10.66], [92.38, 10.79], [92.4, 10.8], [92.41, 10.79], [92.5, 10.89], [92.51, 10.87], [92.52, 10.9], [92.55, 10.88]],
    [[92.83, 12.3], [92.88, 12.3], [92.89, 12.28], [92.9, 12.25], [92.87, 12.24], [92.89, 12.19], [92.85, 12.19], [92.86, 12.16], [92.82, 12.16], [92.82, 12.1], [92.79, 12.1], [92.81, 12.09], [92.77, 12.06], [92.75, 12.09], [92.79, 12.24], [92.77, 12.23], [92.75, 12.25], [92.79, 12.28], [92.78, 12.31], [92.83, 12.3]],
    [[93.54, 8.24], [93.56, 8.22], [93.55, 8.18], [93.51, 8.15], [93.56, 8.09], [93.56, 8.04], [93.52, 8.03], [93.51, 8.0], [93.5, 8.04], [93.52, 8.04], [93.52, 8.07], [93.53, 8.05], [93.55, 8.07], [93.53, 8.08], [93.5, 8.05], [93.5, 8.09], [93.48, 8.1], [93.46, 8.17], [93.5, 8.23], [93.54, 8.24]],
    [[92.98, 12.03], [93.02, 12.02], [93.06, 11.9], [93.05, 11.88], [93.0, 11.93], [93.03, 11.93], [93.01, 11.98], [93.02, 11.96], [93.01, 11.95], [93.0, 11.97], [92.99, 11.94], [92.96, 11.98], [92.93, 11.99], [92.97, 12.05], [92.98, 12.03]],
    [[92.66, 11.49], [92.69, 11.47], [92.69, 11.42], [92.65, 11.4], [92.7, 11.39], [92.7, 11.36], [92.61, 11.34], [92.59, 11.36], [92.6, 11.4], [92.63, 11.4], [92.62, 11.49], [92.64, 11.51], [92.66, 11.49]],
    [[92.71, 12.99], [92.73, 12.89], [92.71, 12.83], [92.69, 12.82], [92.7, 12.81], [92.68, 12.78], [92.66, 12.86], [92.68, 12.88], [92.68, 12.96], [92.71, 12.99]],
    [[93.38, 8.02], [93.4, 8.01], [93.4, 7.97], [93.45, 7.93], [93.46, 7.87], [93.43, 7.9], [93.38, 7.88], [93.34, 7.89], [93.35, 7.94], [93.32, 7.92], [93.32, 7.99], [93.38, 8.02]],
    [[93.74, 7.42], [93.78, 7.37], [93.66, 7.25], [93.64, 7.31], [93.65, 7.37], [93.72, 7.39], [93.72, 7.44], [93.74, 7.42]],
    [[93.13, 8.35], [93.15, 8.35], [93.13, 8.27], [93.21, 8.22], [93.2, 8.2], [93.12, 8.23], [93.1, 8.26], [93.1, 8.33], [93.13, 8.35]],
    [[92.78, 9.25], [92.82, 9.21], [92.83, 9.14], [92.8, 9.12], [92.74, 9.12], [92.72, 9.14], [92.72, 9.21], [92.76, 9.21], [92.78, 9.25]],
    [[93.08, 12.21], [93.1, 12.14], [93.08, 12.08], [93.04, 12.13], [93.08, 12.21]],
    [[93.57, 8.03], [93.59, 7.99], [93.59, 7.93], [93.52, 7.98], [93.54, 8.02], [93.56, 8.0], [93.57, 8.03]],
    [[93.02, 12.99], [92.99, 12.96], [92.99, 12.93], [92.96, 12.93], [92.98, 12.94], [92.96, 12.96], [92.97, 12.99], [92.99, 12.97], [92.99, 12.99], [93.02, 12.99]],
    [[93.03, 12.15], [93.05, 12.04], [93.01, 12.08], [93.01, 12.13], [93.03, 12.16], [93.03, 12.15]],
    [[93.63, 8.53], [93.64, 8.52], [93.65, 8.46], [93.63, 8.45], [93.63, 8.42], [93.63, 8.53]],
    [[92.74, 12.21], [92.75, 12.23], [92.77, 12.22], [92.77, 12.18], [92.73, 12.19], [92.74, 12.24], [92.74, 12.21]],
    [[92.72, 12.83], [92.73, 12.72], [92.7, 12.79], [92.72, 12.83]],
    [[92.23, 11.59], [92.28, 11.57], [92.27, 11.51], [92.23, 11.53], [92.21, 11.58], [92.23, 11.59]],
    [[93.01, 12.1], [93.0, 12.05], [92.97, 12.09], [93.01, 12.1]],
    [[92.95, 12.28], [92.93, 12.23], [92.91, 12.29], [92.94, 12.28], [92.95, 12.31], [92.95, 12.28]],
    [[93.11, 12.24], [93.11, 12.2], [93.07, 12.23], [93.09, 12.26], [93.1, 12.24], [93.11, 12.26], [93.11, 12.24]],
    [[93.6, 8.11], [93.61, 8.04], [93.57, 8.12], [93.59, 8.13], [93.6, 8.11]],
    [[92.55, 11.6], [92.58, 11.58], [92.54, 11.55], [92.55, 11.6]],
    [[92.72, 12.3], [92.74, 12.29], [92.72, 12.23], [92.72, 12.3]],
    [[92.92, 12.24], [92.92, 12.22], [92.9, 12.23], [92.89, 12.21], [92.88, 12.24], [92.92, 12.24]],
    [[93.03, 13.67], [93.04, 13.62], [92.99, 13.65], [93.03, 13.67]],
    [[92.97, 12.41], [92.94, 12.35], [92.93, 12.36], [92.94, 12.41], [92.97, 12.43], [92.97, 12.41]],
    [[92.88, 12.41], [92.9, 12.4], [92.89, 12.37], [92.85, 12.4], [92.88, 12.41]],
    [[93.02, 11.85], [93.08, 11.83], [93.05, 11.81], [93.02, 11.83], [93.02, 11.85]],
    [[92.98, 12.15], [93.0, 12.14], [93.0, 12.11], [92.97, 12.12], [92.98, 12.15]],
    [[93.25, 8.23], [93.24, 8.22], [93.23, 8.26], [93.24, 8.26], [93.25, 8.23]],
    [[92.72, 13.1], [92.73, 13.09], [92.72, 13.06], [92.7, 13.09], [92.7, 13.11], [92.72, 13.1]]];
  const LAKSHADWEEP = [[73.05, 8.29], [72.79, 11.22], [72.19, 10.86], [73.65, 10.08], [73.68, 10.81], [73.01, 11.48], [72.6, 10.56], [72.19, 11.6], [73.66, 10.14], [72.73, 11.12], [72.69, 11.69], [72.53, 10.78], [72.28, 10.04], [72.29, 10.94]];
  const MODES = { explore: '👆 Explore', find: '🔎 Find', latitude: '🧭 Lat / Long' };
  const DIRS = ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west'];
  const R = Math.PI / 180;
  const km = (a, b) => { const dLa = (b[1] - a[1]) * R, dLo = (b[0] - a[0]) * R; const h = Math.sin(dLa / 2) ** 2 + Math.cos(a[1] * R) * Math.cos(b[1] * R) * Math.sin(dLo / 2) ** 2; return 12742 * Math.asin(Math.sqrt(h)); };
  const bearing = (a, b) => { const y = Math.sin((b[0] - a[0]) * R) * Math.cos(b[1] * R), x = Math.cos(a[1] * R) * Math.sin(b[1] * R) - Math.sin(a[1] * R) * Math.cos(b[1] * R) * Math.cos((b[0] - a[0]) * R); return (Math.atan2(y, x) / R + 360) % 360; };
  const dirName = deg => DIRS[Math.round(deg / 45) % 8];
  /* distance (km) from point to polyline, using local flat-earth projection */
  const kmToLine = (pt, pts) => { let best = 1e9; const c = Math.cos(pt[1] * R), P = q => [(q[0] - pt[0]) * 111.2 * c, (q[1] - pt[1]) * 111.2];
    for (let i = 0; i < pts.length - 1; i++) { const a = P(pts[i]), b = P(pts[i + 1]), dx = b[0] - a[0], dy = b[1] - a[1]; let t = -(a[0] * dx + a[1] * dy) / (dx * dx + dy * dy || 1); t = Math.max(0, Math.min(1, t)); best = Math.min(best, Math.hypot(a[0] + t * dx, a[1] + t * dy)); }
    return best; };
  const inPoly = (pt, poly) => { let ins = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > pt[1]) !== (yj > pt[1]) && pt[0] < (xj - xi) * (pt[1] - yi) / (yj - yi) + xi) ins = !ins; } return ins; };
  const fmtLat = v => Math.abs(v).toFixed(1) + '° ' + (v >= 0 ? 'N' : 'S');
  const fmtLon = v => Math.abs(v).toFixed(1) + '° ' + (v >= 0 ? 'E' : 'W');

  Labs.register('indiamap', {
    title: 'India map', subjects: ['social', 'geography', 'evs'],
    render(host, p, api) {
      const ex = this.example || {};
      const places = Array.isArray(p.places) ? p.places : ex.places;
      const lines = Array.isArray(p.lines) ? p.lines : [];
      const regions = Array.isArray(p.regions) ? p.regions : [];
      const modes = (Array.isArray(p.modes) && p.modes.length ? p.modes : [p.mode || 'explore']).filter(m => MODES[m]);
      if (!modes.length) modes.push('explore');
      let mode = modes.includes(p.mode) ? p.mode : modes[0];
      const radius = +p.radius > 0 ? +p.radius : 150;
      const tg = p.target && typeof p.target === 'object' && (p.target.lat != null || p.target.lon != null) ? p.target : { lat: 23.5, lon: 82.5 };
      const target = { lat: tg.lat != null ? +tg.lat : null, lon: tg.lon != null ? +tg.lon : null, tol: +tg.tol > 0 ? +tg.tol : 0.8 };
      /* projection */
      const LON0 = 67.4, LAT1 = 37.7, K = 10.2, CX = Math.cos(22 * R) * K;
      const W = Math.round((97.9 - LON0) * CX), H = Math.round((LAT1 - 6.2) * K);
      const X = lon => (lon - LON0) * CX, Y = lat => (LAT1 - lat) * K;
      const path = pts => pts.map((q, i) => (i ? 'L' : 'M') + X(q[0]).toFixed(1) + ' ' + Y(q[1]).toFixed(1)).join('') ;
      const items = [...places.map(o => ({ kind: 'place', o })), ...lines.map(o => ({ kind: 'line', o })), ...regions.map(o => ({ kind: 'region', o }))];
      const goal = Math.max(1, Math.min(+p.goal || 5, items.length || 1));
      const askNames = (Array.isArray(p.ask) && p.ask.length ? p.ask : places.map(o => o.name)).filter(n => items.some(it => it.o.name === n));
      const rounds = Math.max(1, Math.min(+p.rounds || 4, askNames.length || 1));
      const col = ['#3b82f6', '#8b5cf6', '#ff6b6b', '#2ed3a5', '#ffb020'];

      host.innerHTML = `<div class="lb-indiamap-w"><style>
.lb-indiamap-w{font-size:14px;color:#1b1f3a;user-select:none;-webkit-user-select:none}
.lb-indiamap-ch{font-weight:800;font-size:14px;line-height:1.3;margin-bottom:6px}
.lb-indiamap-tabs{display:flex;gap:6px;margin-bottom:6px}
.lb-indiamap-tabs button{flex:1;min-height:40px;border:none;border-radius:12px;background:#eef0fb;color:#1b1f3a;font:inherit;font-weight:800;font-size:13px;cursor:pointer}
.lb-indiamap-tabs button.on{background:#8b5cf6;color:#fff;box-shadow:0 3px 0 #5b33c9}
.lb-indiamap-stage{position:relative;border-radius:18px;overflow:hidden;background:linear-gradient(180deg,#e9f4ff,#d6ebff)}
.lb-indiamap-stage svg{display:block;width:100%;height:auto;max-height:310px;margin:0 auto}
.lb-indiamap-land{fill:#dff7ea;stroke:#1fae86;stroke-width:1.3;stroke-linejoin:round}
.lb-indiamap-isl{fill:#dff7ea;stroke:#1fae86;stroke-width:1}
.lb-indiamap-sea{fill:#7aa7d6;font-size:9px;font-weight:700;font-style:italic;letter-spacing:.5px}
.lb-indiamap-grid{stroke:#9cc3ea;stroke-width:.6;stroke-dasharray:2 3}
.lb-indiamap-gl{fill:#6f97c4;font-size:7.5px;font-weight:700}
.lb-indiamap-tc{stroke:#ff6b6b;stroke-width:1.6;stroke-dasharray:6 4}
.lb-indiamap-sm{stroke:#8b5cf6;stroke-width:1.6;stroke-dasharray:6 4}
.lb-indiamap-lt{font-size:8px;font-weight:800}
.lb-indiamap-pt{cursor:pointer}
.lb-indiamap-pt .d{fill:#ff6b6b;stroke:#fff;stroke-width:1.6;transition:r .2s}
.lb-indiamap-pt.seen .d{fill:#2ed3a5}
.lb-indiamap-pt.sel .d{fill:#ffc93c;stroke:#1b1f3a}
.lb-indiamap-pt text{font-size:8.5px;font-weight:800;fill:#1b1f3a;paint-order:stroke;stroke:#fff;stroke-width:2.6px;pointer-events:none}
.lb-indiamap-riv{fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;cursor:pointer}
.lb-indiamap-reg{stroke-width:1;cursor:pointer;opacity:.45}
.lb-indiamap-reg.sel{opacity:.75}
.lb-indiamap-card{position:absolute;left:8px;bottom:8px;pointer-events:none;width:47%;background:#fff;border-radius:14px;padding:8px 10px;box-shadow:0 6px 18px rgba(27,31,58,.18);font-size:12.5px;line-height:1.3;transition:opacity .2s}
.lb-indiamap-card b{display:block;font-size:14px;margin-bottom:2px}
.lb-indiamap-card .m{color:#6b7090;font-weight:700;font-size:11.5px}
.lb-indiamap-card:empty{display:none}
.lb-indiamap-card.tr{left:auto;right:8px;bottom:auto;top:38px}
.lb-indiamap-score{position:absolute;right:8px;top:8px;background:#fff;border-radius:999px;padding:4px 10px;font-weight:800;font-size:12px;box-shadow:0 3px 10px rgba(27,31,58,.15)}
.lb-indiamap-score:empty{display:none}
.lb-indiamap-bar{display:flex;align-items:center;gap:8px;margin-top:6px;min-height:42px}
.lb-indiamap-msg{flex:1;font-weight:800;font-size:13.5px;line-height:1.25}
.lb-indiamap-bar button{min-height:40px;border:none;border-radius:12px;padding:0 12px;background:#2ed3a5;color:#fff;font:inherit;font-weight:800;cursor:pointer;box-shadow:0 3px 0 #1a9c78}
.lb-indiamap-pin{pointer-events:none}
.lb-indiamap-ring{fill:none;stroke:#ffc93c;stroke-width:2.5;animation:lb-indiamap-p 1s ease-out infinite}
@keyframes lb-indiamap-p{from{r:3;opacity:1}to{r:18;opacity:0}}
</style>
<div class="lb-indiamap-ch"></div>
${modes.length > 1 ? `<div class="lb-indiamap-tabs">${modes.map(m => `<button data-m="${m}">${MODES[m]}</button>`).join('')}</div>` : ''}
<div class="lb-indiamap-stage"><svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet"></svg><div class="lb-indiamap-card"></div><div class="lb-indiamap-score"></div></div>
<div class="lb-indiamap-bar"><div class="lb-indiamap-msg"></div><button class="lb-indiamap-act" style="display:none"></button></div></div>`;
      const $ = s => host.querySelector(s);
      const svg = $('svg'), card = $('.lb-indiamap-card'), msg = $('.lb-indiamap-msg'), score = $('.lb-indiamap-score'), act = $('.lb-indiamap-act'), chEl = $('.lb-indiamap-ch');
      const NS = 'http://www.w3.org/2000/svg';
      const timers = [];
      let seen = new Set(), prev = null, askQ = [], askI = 0, correct = 0, tries = 0, won = false, pin = [78, 20], dragging = false;

      function toLL(ev) { const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY; const q = pt.matrixTransform(svg.getScreenCTM().inverse()); return [LON0 + q.x / CX, LAT1 - q.y / K]; }
      function itemByName(n) { return items.find(it => it.o.name === n); }
      function showCard(html, ll) {
        card.innerHTML = html;
        let tr = false;
        if (ll) { const r = svg.getBoundingClientRect(), sr = host.querySelector('.lb-indiamap-stage').getBoundingClientRect(); const sx = r.left - sr.left + X(ll[0]) * r.width / W, sy = r.top - sr.top + Y(ll[1]) * r.height / H; tr = sx < sr.width * 0.56 && sy > sr.height - card.offsetHeight - 24; }
        card.classList.toggle('tr', tr);
      }
      function challengeText() {
        if (p.challenge && mode === (modes.includes(p.mode) ? p.mode : modes[0])) return p.challenge;
        if (mode === 'explore') return `Tap ${goal} different places on the map to learn about them`;
        if (mode === 'find') return `Find ${rounds} places on the map — tap where you think each one is`;
        if (target.lat != null && target.lon != null) return `Drag the pin to ${fmtLat(target.lat)}, ${fmtLon(target.lon)}` + (target.lat === 23.5 && target.lon === 82.5 ? ' — where the Tropic of Cancer meets the Standard Meridian' : '');
        return target.lat != null ? `Drag the pin onto latitude ${fmtLat(target.lat)}` : `Drag the pin onto longitude ${fmtLon(target.lon)}`;
      }
      function draw() {
        const showGrid = p.grid != null ? !!p.grid : mode === 'latitude';
        let s = '';
        if (showGrid) {
          for (let la = 10; la <= 30; la += 5) s += `<line class="lb-indiamap-grid" x1="0" x2="${W}" y1="${Y(la)}" y2="${Y(la)}"/><text class="lb-indiamap-gl" x="2" y="${Y(la) - 2}">${la}°N</text>`;
          for (let lo = 70; lo <= 95; lo += 5) s += `<line class="lb-indiamap-grid" y1="0" y2="${H}" x1="${X(lo)}" x2="${X(lo)}"/><text class="lb-indiamap-gl" x="${X(lo) + 2}" y="${H - 3}">${lo}°E</text>`;
        }
        s += `<text class="lb-indiamap-sea" x="${X(69.2)}" y="${Y(17.2)}">Arabian</text><text class="lb-indiamap-sea" x="${X(69.6)}" y="${Y(16.3)}">Sea</text>`;
        s += `<text class="lb-indiamap-sea" x="${X(85.6)}" y="${Y(15.8)}">Bay of</text><text class="lb-indiamap-sea" x="${X(85.4)}" y="${Y(14.9)}">Bengal</text>`;
        s += `<text class="lb-indiamap-sea" x="${X(82.0)}" y="${Y(7.0)}">Indian Ocean</text>`;
        s += `<path class="lb-indiamap-land" d="${path(MAIN)}Z"/>`;
        ISLANDS.forEach(pl => { s += `<path class="lb-indiamap-isl" d="${path(pl)}Z"/>`; });
        LAKSHADWEEP.forEach(q => { s += `<circle class="lb-indiamap-isl" cx="${X(q[0])}" cy="${Y(q[1])}" r="1.8"/>`; });
        regions.forEach((r, i) => { if (Array.isArray(r.pts)) s += `<path class="lb-indiamap-reg" data-k="region" data-i="${i}" fill="${esc(r.color || col[i % 5])}" stroke="${esc(r.color || col[i % 5])}" d="${path(r.pts)}Z"/>`; });
        if (p.tropic !== false) s += `<line class="lb-indiamap-tc" x1="0" x2="${W}" y1="${Y(23.44)}" y2="${Y(23.44)}"/><text class="lb-indiamap-lt" fill="#e04848" x="${X(92.6)}" y="${Y(23.44) - 3}">Tropic of Cancer</text><line data-k="tropic" x1="0" x2="${W}" y1="${Y(23.44)}" y2="${Y(23.44)}" stroke="transparent" stroke-width="12"/>`;
        if (p.meridian !== false) s += `<line class="lb-indiamap-sm" y1="0" y2="${H}" x1="${X(82.5)}" x2="${X(82.5)}"/><text class="lb-indiamap-lt" fill="#7044e0" x="${X(82.5) + 3}" y="${Y(9.2)}">82.5°E</text><line data-k="meridian" y1="0" y2="${H}" x1="${X(82.5)}" x2="${X(82.5)}" stroke="transparent" stroke-width="12"/>`;
        lines.forEach((l, i) => { if (Array.isArray(l.pts)) s += `<path class="lb-indiamap-riv" stroke="${esc(l.color || '#3b82f6')}" d="${path(l.pts)}"/><path data-k="line" data-i="${i}" d="${path(l.pts)}" fill="none" stroke="transparent" stroke-width="14"/>`; });
        const showLabels = mode === 'explore' && p.labels !== false;
        const boxes = [];
        places.forEach((o, i) => {
          const x = X(+o.lon), y = Y(+o.lat), label = (o.emoji ? o.emoji + ' ' : '') + o.name, lw = label.length * 4.6 + 6;
          let lab = '';
          if (showLabels) {
            const cands = [[x + 6, y + 3, 'start'], [x - 6, y + 3, 'end'], [x + 6, y + 12, 'start'], [x + 6, y - 6, 'start'], [x - 6, y + 12, 'end'], [x - 6, y - 6, 'end']];
            if (o.side === 'l' || +o.lon > 89) cands.unshift(cands.splice(1, 1)[0]);
            const box = c => { const x0 = c[2] === 'start' ? c[0] : c[0] - lw; return [x0, c[1] - 8, x0 + lw, c[1] + 2]; };
            const hit = b => b[0] < 0 || b[2] > W || boxes.some(q => b[0] < q[2] && b[2] > q[0] && b[1] < q[3] && b[3] > q[1]) || places.some(q => q !== o && Math.abs(X(+q.lon) - Math.max(b[0], Math.min(b[2], X(+q.lon)))) < 3 && Math.abs(Y(+q.lat) - Math.max(b[1], Math.min(b[3], Y(+q.lat)))) < 3);
            const c = cands.find(c => !hit(box(c))) || cands[0]; boxes.push(box(c));
            lab = `<text x="${c[0]}" y="${c[1]}" text-anchor="${c[2]}">${esc(label)}</text>`;
          }
          s += `<g class="lb-indiamap-pt${seen.has('place' + i) ? ' seen' : ''}" data-k="place" data-i="${i}"><circle cx="${x}" cy="${y}" r="13" fill="transparent"/><circle class="d" cx="${x}" cy="${y}" r="${mode === 'find' ? 0 : 4.2}"/>${lab}</g>`;
        });
        s += `<g class="lb-indiamap-fx"></g>`;
        s += `<g transform="translate(18,24)"><circle r="13" fill="#fff" opacity=".85"/><path d="M0 -10 L4 0 L0 -2 L-4 0Z" fill="#ff6b6b"/><path d="M0 10 L4 0 L0 2 L-4 0Z" fill="#9aa0c0"/><text y="-13" text-anchor="middle" font-size="8" font-weight="800" fill="#1b1f3a">N</text></g>`;
        if (mode === 'latitude') s += `<g class="lb-indiamap-pin"><line class="pl1" stroke="#1b1f3a" stroke-width=".8" stroke-dasharray="3 2"/><line class="pl2" stroke="#1b1f3a" stroke-width=".8" stroke-dasharray="3 2"/><g class="ph"><circle r="16" fill="#ffc93c" opacity=".3"/><path d="M0 0 C-7 -9 -7 -17 0 -17 C7 -17 7 -9 0 0Z" fill="#ff6b6b" stroke="#fff" stroke-width="1.5"/><circle cy="-12" r="2.6" fill="#fff"/></g></g>`;
        svg.innerHTML = s;
        svg.style.touchAction = mode === 'latitude' ? 'none' : '';
        if (mode === 'latitude') movePin();
      }
      function fx(lon, lat, color) { const g = svg.querySelector('.lb-indiamap-fx'); if (!g) return; const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', X(lon)); c.setAttribute('cy', Y(lat)); c.setAttribute('r', 3); c.setAttribute('class', 'lb-indiamap-ring'); if (color) c.style.stroke = color; g.appendChild(c); timers.push(setTimeout(() => c.remove(), 1900)); }
      function info(it, i) {
        const o = it.o; let extra = '';
        if (it.kind === 'place') {
          extra = `<div class="m">${fmtLat(+o.lat)}, ${fmtLon(+o.lon)}</div>`;
          if (prev && prev.o !== o && prev.kind === 'place') extra += `<div class="m">${esc(o.name)} is ${dirName(bearing([+prev.o.lon, +prev.o.lat], [+o.lon, +o.lat]))} of ${esc(prev.o.name)}, ~${Math.round(km([+prev.o.lon, +prev.o.lat], [+o.lon, +o.lat]) / 10) * 10} km</div>`;
        }
        const at = it.kind === 'place' ? [+o.lon, +o.lat] : (Array.isArray(o.pts) && o.pts.length ? o.pts[o.pts.length >> 1] : null);
        showCard(`<b>${esc((o.emoji ? o.emoji + ' ' : '') + o.name)}</b>${o.info ? esc(o.info) : ''}${extra}`, at);
      }
      function tapItem(kind, i) {
        const it = items.find(t => t.kind === kind && t.o === ({ place: places, line: lines, region: regions }[kind])[i]); if (!it) return;
        api.sfx('tap'); info(it, i); seen.add(kind + i); prev = it;
        svg.querySelectorAll('.sel').forEach(e => e.classList.remove('sel'));
        const g = svg.querySelector(`[data-k="${kind}"][data-i="${i}"]`); if (g) g.classList.add('sel', 'seen');
        if (kind === 'place') { fx(+it.o.lon, +it.o.lat); if (it.o.info) api.speak(it.o.name + '. ' + it.o.info); else api.speak(it.o.name); }
        score.textContent = `⭐ ${Math.min(seen.size, goal)} / ${goal}`;
        if (!won && seen.size >= goal) { won = true; msg.textContent = 'Great exploring! 🎉'; api.win(`You explored ${goal} places on the map of India!`); }
        else if (!won) msg.textContent = `Tap ${goal - seen.size} more`;
      }
      function nextAsk() {
        if (!askQ.length) { msg.textContent = 'Add places to ask about.'; return; }
        const it = itemByName(askQ[askI % askQ.length]); tries = 0;
        msg.innerHTML = `Where is <span style="color:#8b5cf6">${esc((it.o.emoji ? it.o.emoji + ' ' : '') + it.o.name)}</span>? Tap the map.`;
        score.textContent = `✅ ${correct} / ${rounds}`; act.style.display = 'none';
      }
      function judge(ll) {
        const it = itemByName(askQ[askI % askQ.length]); if (!it) return;
        let d, ok, ref;
        if (it.kind === 'place') { ref = [+it.o.lon, +it.o.lat]; d = km(ll, ref); ok = d <= radius; }
        else if (it.kind === 'line') { d = kmToLine(ll, it.o.pts); ok = d <= Math.max(60, radius / 2); ref = it.o.pts[Math.floor(it.o.pts.length / 2)]; }
        else { ok = inPoly(ll, it.o.pts); d = ok ? 0 : 999; const c = it.o.pts.reduce((a, q) => [a[0] + q[0] / it.o.pts.length, a[1] + q[1] / it.o.pts.length], [0, 0]); ref = c; d = ok ? 0 : km(ll, c); }
        tries++;
        if (ok) {
          correct++; api.sfx('correct'); fx(ref[0], ref[1], '#2ed3a5');
          const i = ({ place: places, line: lines, region: regions })[it.kind].indexOf(it.o); const g = svg.querySelector(`[data-k="${it.kind}"][data-i="${i}"]`);
          if (g) { g.classList.add('seen'); const dot = g.querySelector('.d'); if (dot) dot.setAttribute('r', 4.2); }
          showCard(`<b>✅ ${esc((it.o.emoji ? it.o.emoji + ' ' : '') + it.o.name)}</b>${it.o.info ? esc(it.o.info) : ''}`, ref);
          score.textContent = `✅ ${correct} / ${rounds}`;
          if (correct >= rounds) { if (!won) { won = true; msg.textContent = 'You found them all! 🎉'; api.win(`You found ${rounds} places on the map of India!`); } act.textContent = 'Play again'; act.style.display = ''; return; }
          askI++; msg.textContent = 'Correct!'; timers.push(setTimeout(nextAsk, 1100));
        } else {
          api.sfx('wrong');
          const dir = dirName(bearing(ll, ref));
          if (tries >= 3) {
            fx(ref[0], ref[1], '#ff6b6b');
            const i = ({ place: places, line: lines, region: regions })[it.kind].indexOf(it.o); const g = svg.querySelector(`[data-k="${it.kind}"][data-i="${i}"] .d`); if (g) g.setAttribute('r', 4.2);
            msg.innerHTML = `It was here 👆 (go ${dir}). Next one!`; askI++; timers.push(setTimeout(nextAsk, 2200));
          } else msg.innerHTML = `Not quite — about ${Math.round(d / 10) * 10} km away. Go <b>${dir}</b>.`;
        }
      }
      function movePin() {
        const x = X(pin[0]), y = Y(pin[1]);
        const ph = svg.querySelector('.ph'); if (!ph) return; ph.setAttribute('transform', `translate(${x},${y})`);
        const l1 = svg.querySelector('.pl1'), l2 = svg.querySelector('.pl2');
        l1.setAttribute('x1', 0); l1.setAttribute('x2', W); l1.setAttribute('y1', y); l1.setAttribute('y2', y);
        l2.setAttribute('y1', 0); l2.setAttribute('y2', H); l2.setAttribute('x1', x); l2.setAttribute('x2', x);
        const min = Math.round((pin[0] - 82.5) * 4), tc = pin[1] > 23.44 ? 'north' : 'south';
        const onLand = inPoly(pin, MAIN) || ISLANDS.some(pl => inPoly(pin, pl));
        showCard(`<b>📍 ${fmtLat(pin[1])}, ${fmtLon(pin[0])}</b>${Math.abs(pin[1] - 23.44) < 0.3 ? 'On the Tropic of Cancer!' : `${tc === 'north' ? '⬆️' : '⬇️'} ${tc} of the Tropic of Cancer`}<div class="m">${Math.abs(min) < 2 ? 'On the Standard Meridian: Sun time = IST' : `Sun time is ${Math.abs(min)} min ${min > 0 ? 'ahead of' : 'behind'} IST`}</div><div class="m">${onLand ? 'In India 🇮🇳' : 'In the sea / outside India 🌊'}</div>`, pin);
        if (!won) {
          const okLa = target.lat == null || Math.abs(pin[1] - target.lat) <= target.tol, okLo = target.lon == null || Math.abs(pin[0] - target.lon) <= target.tol;
          if (okLa && okLo && !dragging) { won = true; api.sfx('correct'); fx(pin[0], pin[1], '#2ed3a5'); msg.textContent = 'Spot on! 🎉'; api.win(`You placed the pin at ${fmtLat(pin[1])}, ${fmtLon(pin[0])}!`); }
          else if (!dragging) msg.textContent = hintLat();
        }
      }
      function hintLat() {
        const h = [];
        if (target.lat != null && Math.abs(pin[1] - target.lat) > target.tol) h.push(pin[1] < target.lat ? 'north ⬆️' : 'south ⬇️');
        if (target.lon != null && Math.abs(pin[0] - target.lon) > target.tol) h.push(pin[0] < target.lon ? 'east ➡️' : 'west ⬅️');
        return h.length ? 'Move ' + h.join(' and ') : '';
      }
      function setMode(m) {
        mode = m; won = false; api.resetWin && api.resetWin(); seen = new Set(); prev = null; correct = 0; askI = 0; card.innerHTML = ''; score.textContent = ''; act.style.display = 'none';
        host.querySelectorAll('.lb-indiamap-tabs button').forEach(b => b.classList.toggle('on', b.dataset.m === m));
        chEl.textContent = '🎯 Challenge: ' + challengeText();
        draw();
        if (m === 'explore') { msg.textContent = items.length ? 'Tap a dot, river or area 👆' : 'No places given.'; score.textContent = `⭐ 0 / ${goal}`; }
        else if (m === 'find') { askQ = askNames.slice().sort(() => Math.random() - .5); nextAsk(); }
        else { pin = [76, 15]; movePin(); msg.textContent = 'Drag the pin 📍 ' + hintLat(); }
      }
      function onDown(ev) {
        if (mode === 'latitude') { dragging = true; svg.setPointerCapture && svg.setPointerCapture(ev.pointerId); onMove(ev); return; }
        const t = ev.target.closest && ev.target.closest('[data-k]');
        if (mode === 'explore') {
          if (!t) return;
          const k = t.dataset.k;
          if (k === 'tropic') { api.sfx('tap'); showCard('<b>Tropic of Cancer · 23.5° N</b>Passes through 8 states: Gujarat, Rajasthan, Madhya Pradesh, Chhattisgarh, Jharkhand, West Bengal, Tripura and Mizoram.'); return; }
          if (k === 'meridian') { api.sfx('tap'); showCard('<b>Standard Meridian · 82.5° E</b>Passes near Mirzapur (UP). India\'s time (IST) is set here: 82.5 ÷ 15 = 5½ hours ahead of GMT.'); return; }
          tapItem(k, +t.dataset.i);
        } else if (mode === 'find') {
          if (won && correct >= rounds) return;
          if (act.style.display === '' ) return;
          const ll = toLL(ev); fx(ll[0], ll[1], '#8b5cf6'); judge(ll);
        }
      }
      function onMove(ev) { if (!dragging) return; const ll = toLL(ev); pin = [Math.max(68, Math.min(97.5, ll[0])), Math.max(6.5, Math.min(37.3, ll[1] + 0.9))]; movePin(); msg.textContent = hintLat() ? 'Move ' + hintLat().replace('Move ', '') : 'Let go here!'; }
      function onUp() { if (!dragging) return; dragging = false; movePin(); }
      svg.addEventListener('pointerdown', onDown); svg.addEventListener('pointermove', onMove); svg.addEventListener('pointerup', onUp); svg.addEventListener('pointercancel', onUp);
      host.querySelectorAll('.lb-indiamap-tabs button').forEach(b => b.addEventListener('click', () => { api.sfx('tap'); setMode(b.dataset.m); }));
      act.addEventListener('click', () => { api.sfx('tap'); setMode(mode); });
      setMode(mode);
      return () => { timers.forEach(clearTimeout); svg.removeEventListener('pointerdown', onDown); };
    },
    example: {
      title: 'Cities and rivers of India', mode: 'explore', modes: ['explore', 'find', 'latitude'],
      challenge: 'Tap 5 different places and rivers to learn about them',
      places: [
        { name: 'New Delhi', lat: 28.61, lon: 77.21, emoji: '🏛️', info: 'Capital of India.' },
        { name: 'Mumbai', lat: 19.08, lon: 72.88, emoji: '⚓', info: 'Big port city on the west coast.' },
        { name: 'Kolkata', lat: 22.57, lon: 88.36, emoji: '🌉', info: 'City on the Hooghly river, near the Bay of Bengal.' },
        { name: 'Chennai', lat: 13.08, lon: 80.27, emoji: '🏖️', info: 'Capital of Tamil Nadu, on the east coast.' },
        { name: 'Bengaluru', lat: 12.97, lon: 77.59, emoji: '💻', info: 'Capital of Karnataka, on the Deccan plateau.' },
        { name: 'Srinagar', lat: 34.08, lon: 74.80, emoji: '🏔️', info: 'Summer capital of Jammu & Kashmir, on the Jhelum.' },
        { name: 'Leh', lat: 34.15, lon: 77.58, emoji: '🗻', info: 'Main town of Ladakh, high in the mountains.' },
        { name: 'Guwahati', lat: 26.14, lon: 91.74, emoji: '🛶', info: 'Largest city of Assam, on the Brahmaputra.' },
        { name: 'Jaipur', lat: 26.91, lon: 75.79, emoji: '🐪', info: 'Pink City, capital of Rajasthan.' },
        { name: 'Kanyakumari', lat: 8.08, lon: 77.55, emoji: '🌅', info: 'Southern tip of mainland India.' },
        { name: 'Port Blair', lat: 11.62, lon: 92.73, emoji: '🏝️', info: 'Capital of Andaman & Nicobar Islands.' },
        { name: 'Kavaratti', lat: 10.57, lon: 72.64, emoji: '🐠', info: 'Capital of Lakshadweep (coral islands).' }
      ],
      lines: [
        { name: 'Ganga', color: '#3b82f6', info: 'Starts at Gangotri glacier and flows east to the Bay of Bengal.', pts: [[78.9, 30.95], [78.3, 30.1], [78.16, 29.95], [79.4, 28.4], [80.35, 26.45], [81.85, 25.43], [83.0, 25.3], [85.1, 25.6], [86.5, 25.3], [87.9, 24.8], [88.3, 23.5], [88.2, 22.5], [88.1, 21.7]] },
        { name: 'Brahmaputra', color: '#0ea5e9', info: 'Enters India in Arunachal Pradesh and flows west through Assam.', pts: [[95.3, 28.3], [95.2, 27.8], [94.9, 27.5], [93.8, 26.8], [92.7, 26.5], [91.74, 26.2], [90.6, 26.2], [89.9, 26.0]] },
        { name: 'Narmada', color: '#6366f1', info: 'Rises at Amarkantak and flows WEST into the Arabian Sea.', pts: [[81.75, 22.67], [80.6, 22.9], [79.9, 23.15], [78.7, 22.8], [77.5, 22.6], [76.0, 22.2], [74.4, 22.0], [73.0, 21.7], [72.6, 21.65]] },
        { name: 'Godavari', color: '#14b8a6', info: 'Longest river of peninsular India; rises near Nashik.', pts: [[73.5, 19.95], [75.0, 19.5], [76.8, 19.1], [78.3, 18.9], [79.9, 18.8], [80.9, 17.9], [81.8, 17.0], [82.3, 16.6]] }
      ],
      regions: [], ask: ['New Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Srinagar', 'Guwahati', 'Kanyakumari', 'Ganga'], rounds: 4, radius: 160, goal: 5
    },
    examples: [
      { title: 'Latitude and time in India (Class 9)', mode: 'latitude', modes: ['latitude', 'explore'],
        challenge: 'Drag the pin to where the Tropic of Cancer meets the Standard Meridian (82.5° E)',
        target: { lat: 23.5, lon: 82.5, tol: 0.8 }, grid: true, goal: 3,
        places: [{ name: 'Mirzapur', lat: 25.15, lon: 82.57, emoji: '⏰', info: 'IST is measured along 82.5° E, near Mirzapur.' },
          { name: 'Indira Point', lat: 6.75, lon: 93.84, emoji: '📍', info: 'Southernmost point of India (Great Nicobar).' },
          { name: 'Kibithu', lat: 28.0, lon: 97.0, emoji: '🌄', info: 'In Arunachal Pradesh — the Sun rises here about 2 hours before Gujarat.' },
          { name: 'Guhar Moti', lat: 23.7, lon: 68.1, emoji: '🌇', info: 'Westernmost point, in Kutch, Gujarat.' }],
        lines: [], regions: [], ask: [] },
      { title: 'Find the state capitals (Class 4-5)', mode: 'find', modes: ['find', 'explore'],
        challenge: 'Find 4 state capitals — tap where you think each one is', radius: 180, rounds: 4, grid: false,
        places: [{ name: 'Lucknow', lat: 26.85, lon: 80.95, emoji: '🕌' }, { name: 'Bhopal', lat: 23.26, lon: 77.41, emoji: '🌊', info: 'City of Lakes.' },
          { name: 'Patna', lat: 25.59, lon: 85.14, emoji: '🏯' }, { name: 'Thiruvananthapuram', lat: 8.52, lon: 76.94, emoji: '🌴' },
          { name: 'Gandhinagar', lat: 23.22, lon: 72.65, emoji: '🦁' }, { name: 'Shimla', lat: 31.10, lon: 77.17, emoji: '🍎' },
          { name: 'Bhubaneswar', lat: 20.30, lon: 85.82, emoji: '🛕' }, { name: 'Dispur', lat: 26.14, lon: 91.79, emoji: '🍵' }],
        lines: [], regions: [{ name: 'Thar Desert', color: '#ffc93c', info: 'Hot sandy desert in Rajasthan.', pts: [[69.8, 27.2], [71.5, 28.6], [73.6, 29.4], [74.4, 27.6], [73.5, 25.4], [71.2, 25.0], [70.4, 25.9]] }], ask: [] }
    ]
  });
})();

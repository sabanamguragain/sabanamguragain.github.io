/* ============================================================
   Underlying data for the interactive dashboards.
   Economic figures: Nepal Rastra Bank, Current Macroeconomic
   Situation (annual data, FY 2020/21–2024/25).
   Education/disability figures: CBS Census 2021, MoEST Flash
   Reports 2024/25, UNICEF, UNESCO-UIS, Washington Group.
   ============================================================ */

const FY = ['2020/21', '2021/22', '2022/23', '2023/24', '2024/25'];

const ECON = {
  years: FY,
  realGdpGrowth:   [4.84, 5.63, 1.98, 3.67, 4.61],        // %
  nominalGdp:      [4352.55, 4976.56, 5367, 5709.1, 6107.22], // Rs. Billion
  cpiOverall:      [4.19, 8.08, 7.44, 3.57, 2.20],        // %
  cpiFood:         [5.94, 6.70, 7.01, 4.04, -1.19],
  cpiNonFood:      [3.04, 9.01, 7.72, 3.26, 4.12],
  exports:         [141.12, 200.03, 157.14, 152.38, 277.03], // Rs. Billion
  imports:         [1539.84, 1920.45, 1611.73, 1592.99, 1804.12],
  remittances:     [961.05, 1007.31, 1240.69, 1445.32, 1723.27], // Rs. Billion
  forex:           [11752.56, 9512.57, 11708.85, 15270.86, 19502.43], // USD Million
  revenueGrowth:   [16.0, 14.1, -9.3, 7.1, 10.5],         // %
  expenditureGrowth:[9.7, 9.5, 8.5, -2.0, 9.3],
  domesticDebt:    [800.32, 984.29, 1129.1, 1180.9, 1268.22], // Rs. Billion
  externalDebt:    [934.15, 1025.85, 1170.25, 1257.87, 1401.42],
  tbill91:         [4.55, 10.66, 6.35, 3.00, 2.95],       // %
  lendingRate:     [8.43, 11.62, 12.30, 9.93, 7.85],
  nepse:           [2883.41, 2009.47, 2097.1, 2240.41, 2794.79], // index close
  // GDP composition by sector, 2024/25 current prices (%)
  sectorLabels: ['Agriculture', 'Wholesale/Retail', 'Public Admin', 'Education', 'Transport', 'Construction', 'Manufacturing', 'Others'],
  sectorShare:  [25.2, 12.8, 7.7, 6.9, 6.3, 4.6, 4.4, 32.1],
  // Per capita income (NRs.)
  perCapitaLabels: ['Per Capita GDP', 'Per Capita GNI', 'Per Capita GNDI'],
  perCapita2024: [192031, 195183, 248033],
  perCapita2025: [203538, 206424, 263959],
};

const EDU = {
  // Literacy rate by category, age 5+ (Census 2021), %
  literacyLabels: ['Overall', 'Male', 'Female', 'Urban', 'Rural'],
  literacy:       [76, 84, 69, 85, 72],
  // Children with disabilities as % of total enrolment, by level (Flash)
  cwdLevels: ['Pre-primary', 'Primary', 'Secondary', 'Higher Sec.'],
  cwdShare:  [0.34, 0.94, 0.88, 0.45],
  cwdExpectedLow: 5,   // estimated prevalence band, %
  // Barriers to education for children with disabilities (% citing), horizontal
  barrierLabels: ['Physical inaccessibility', 'Untrained teachers', 'Lack of assistive devices', 'Social stigma', 'Inadequate funding', 'Non-inclusive curriculum'],
  barriers:      [85, 78, 72, 68, 65, 58],
  // Gender Parity Index by level (Flash 2024/25); 1.0 = parity
  gpiLevels: ['Primary', 'Basic (1–8)', 'Secondary'],
  gpi:       [1.01, 1.00, 0.93],
};

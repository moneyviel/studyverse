"""CA Intermediate · Paper 4 Cost and Management Accounting · Chapter 12 Service Costing.
Scope follows the ICAI study material; explanations, names and figures are original and machine-checked."""
from ikit import *

UID = 'int-p4-ch12-u01'
T1 = 'Features of service costing and cost units'
T2 = 'Transport costing'
T3 = 'Hotels, hospitals and other services'


def build():
    ck = Checks()
    atk = ck.add('8*100+5*60', 'Absolute tonne-km')
    ctk = ck.add('(8+5)/2*(100+60)', 'Commercial tonne-km')
    cost = ck.add('(4800+3000+1500)', 'Trip cost (fuel, driver, other)')
    rate = ck.add('9300/1100', 'Cost per absolute tonne-km')
    i1 = {'id': 'i1', 'title': 'Measuring a truck\'s work', 'difficulty': 'moderate', 'minutes': 8,
          'q': 'A truck carries 8 tonnes from Nashik to Pune (100 km) and unloads it all; it then carries 5 tonnes from Pune to Satara (60 km). Trip costs: fuel ₹4,800, driver ₹3,000, other ₹1,500. Compute absolute and commercial tonne-km and cost per absolute tonne-km.',
          'solution': [table(['Measure', 'Working', 'Value'], [
              ['Absolute tonne-km', '8 × 100 + 5 × 60', inr(atk)],
              ['Commercial tonne-km', 'Average load (8 + 5) ÷ 2 × total distance 160 km', inr(ctk)],
              ['Trip cost', '4,800 + 3,000 + 1,500', '₹' + inr(cost)],
              ['Cost per absolute tonne-km', '9,300 ÷ 1,100', '₹' + str(round(rate, 2))]], title='Composite cost units')],
          'checks': list(ck)}

    ck2 = Checks()
    rd = ck2.add('50*360*80/100', 'Room-days occupied')
    cpd = ck2.add('11520000/14400', 'Cost per room-day')
    rent = ck2.add('800*1.2', 'Rent per room-day for 20% profit on cost')
    i2 = {'id': 'i2', 'title': 'Pricing a hotel room', 'difficulty': 'moderate', 'minutes': 7,
          'q': 'Lakeview Hotel has 50 rooms, open 360 days a year, with expected occupancy of 80%. Total annual cost is ₹1,15,20,000. Compute cost per room-day and the room rent to earn 20% on cost.',
          'solution': [table(['Item', 'Working', 'Value'], [
              ['Room-days occupied', '50 × 360 × 80%', inr(rd)],
              ['Cost per room-day', '1,15,20,000 ÷ 14,400', '₹' + inr(cpd)],
              ['Rent per room-day', '800 × 120%', '₹' + inr(rent)]], title='Hotel costing')],
          'checks': list(ck2)}

    concepts = [
        C('c1', T1, [
            'Service costing (operating costing) finds the cost of services such as transport, power, hotels, hospitals, education, IT and toll roads. Services cannot be stored, are largely fixed-cost businesses, and need cost units that capture the work done.',
            'Composite cost units combine two measures: passenger-km, tonne-km, room-day, patient-day, kilowatt-hour, student-hour, vehicle-km.',
            'Costs are classified as fixed (standing) charges, semi-variable (maintenance) charges and variable (running) charges, and collected on a log sheet or service cost sheet.'],
          'A good cost unit captures both "how much" and "how far" or "how long".',
          'A bus company uses passenger-km because both passengers carried and distance matter.'),
        C('c2', T2, [
            'Absolute tonne-km (or passenger-km) = sum of (load × distance) for each leg.',
            'Commercial tonne-km = average load × total distance, where average load is the simple average of loads on the legs.',
            'Standing charges: garage rent, insurance, road tax, driver\'s salary, depreciation (if time-based); running charges: fuel, oil, tyres, depreciation (if usage-based); maintenance: repairs, servicing. Fare or freight = cost per unit plus profit margin.'],
          'Absolute tonne-km tracks each leg exactly; commercial tonne-km uses the average.',
          'A bus with 40 passengers for 50 km does 2,000 passenger-km.'),
        C('c3', T3, [
            'Hotels: room-day or bed-night; occupancy rate is crucial, and costs such as laundry, food and housekeeping are separated by department.',
            'Hospitals: patient-day or bed-day for wards; per test for labs; per procedure for operation theatres. Idle capacity costs must be watched.',
            'Other services: power (kWh), education (student-year), IT and ITeS (per user or per transaction), toll roads (per vehicle crossing; build-operate-transfer model needs recovery of investment over the concession period).'],
          'Pricing a service is recovering largely fixed costs over expected usage.',
          'A 100-bed hospital at 75% occupancy over 365 days provides 27,375 patient-days.'),
    ]

    jobs = [{'id': 'j1', 'title': 'Freight rate setting', 'role': 'Cost accountant trainee',
             'situation': 'A fleet owner wants a freight rate per tonne-km for a new route.',
             'steps': ['Estimate distance and loads per leg.', 'Classify costs as standing, running and maintenance.', 'Compute cost per tonne-km.', 'Add margin and compare with market rates.'],
             'takeaway': 'Empty return trips raise cost per tonne-km sharply.'}]

    mcqs = [
        Q('m1', 'The cost unit for a hospital ward is usually:', ['Patient-day', 'Tonne-km', 'Kilowatt-hour', 'Room-day'], 0,
          'Patient-day (or bed-day) captures patients and time. In practice: labs use cost per test.', 'c1', T1),
        Q('m2', 'A bus carries 30 passengers for 40 km and 20 passengers for 60 km. Passenger-km:', ['2,400', '5,000', '3,000', '1,200'], 0,
          '30 × 40 + 20 × 60 = 1,200 + 1,200 = 2,400. In practice: use for fare per passenger-km.', 'c2', T2, check=2400),
        Q('m3', 'Commercial tonne-km is calculated as:', ['Average load × total distance', 'Sum of load × distance per leg', 'Maximum load × distance', 'Load × time'], 0,
          'The average of loads on each leg multiplied by total distance. In practice: absolute tonne-km is leg-wise.', 'c2', T2),
        Q('m4', 'Which is a standing charge in transport costing?', ['Insurance', 'Fuel', 'Tyres', 'Lubricants'], 0,
          'Insurance is fixed regardless of distance. The others vary with running. In practice: driver salary is usually standing.', 'c2', T2),
        Q('m5', 'Hotel with 40 rooms, 300 days, 75% occupancy. Room-days:', ['9,000', '12,000', '7,500', '10,000'], 0,
          '40 × 300 × 75% = 9,000. In practice: divide total cost by this.', 'c3', T3, check=9000),
        Q('m6', 'Service costing is also called:', ['Operating costing', 'Batch costing', 'Contract costing', 'Marginal costing'], 0,
          'Operating costing applies to services. In practice: power and transport are common examples.', 'c1', T1),
        Q('m7', 'Cost per room-day ₹1,000; required profit 25% on rent. Rent:', ['₹1,333', '₹1,250', '₹1,200', '₹1,500'], 0,
          '1,000 ÷ 0.75 = ₹1,333. In practice: 25% on cost would give ₹1,250.', 'c3', T3, 'moderate', check=1333),
        Q('m8', 'Toll road costing under BOT recovers:', ['Construction and operating costs over the concession period', 'Only maintenance costs', 'Only fuel costs', 'Nothing'], 0,
          'Build-operate-transfer projects price tolls to recover investment and running costs before handover. In practice: traffic forecasts drive the toll.', 'c3', T3),
    ]

    questions = [
        W('q1', 5, i1['q'], i1['solution'],
          [S('s1', 'Absolute tonne-km', 2, 'computation', 'absolute', nums=[atk]), S('s2', 'Commercial tonne-km', 2, 'computation', 'commercial', nums=[ctk]), S('s3', 'Cost per unit', 1, 'computation', 'per', nums=[rate])],
          ['Show each leg.'], ['Mixing up the two measures.'], ['Table.'], pad='table', checks=list(ck)),
        W('q2', 4, i2['q'], i2['solution'],
          [S('s1', 'Room-days', 2, 'computation', 'room-days', nums=[rd]), S('s2', 'Cost and rent', 2, 'computation', 'rent', nums=[cpd, rent])],
          ['Apply occupancy.'], ['Ignoring occupancy.'], ['Table.'], pad='table', checks=list(ck2)),
    ]

    viva = [
        V('v1', 'What is a composite cost unit?', 'A unit combining two measures of service, such as tonne-km or patient-day, to capture both volume and distance or time.',
          [P('p1', 'Two measures', 6, 'two|combin'), P('p2', 'Example', 4, 'tonne-km|patient-day|passenger')], 'c1'),
        V('v2', 'How is absolute tonne-km computed?', 'By multiplying the load carried on each leg by the distance of that leg and adding the products.',
          [P('p1', 'Each leg', 5, 'each leg|leg'), P('p2', 'Load × distance', 5, 'load|distance')], 'c2'),
        V('v3', 'Name two running charges in transport.', 'Fuel and lubricants, along with tyres and usage-based depreciation.',
          [P('p1', 'Fuel', 5, 'fuel'), P('p2', 'Others', 5, 'lubricant|tyre|oil')], 'c2'),
        V('v4', 'Why is occupancy important in hotel costing?', 'Because costs are largely fixed, so cost per room-day depends on how many rooms are actually occupied.',
          [P('p1', 'Fixed costs', 5, 'fixed'), P('p2', 'Occupied rooms', 5, 'occupied|occupancy')], 'c3'),
        V('v5', 'What is the cost unit for power generation?', 'The kilowatt-hour of electricity generated or supplied.',
          [P('p1', 'kWh', 6, 'kilowatt'), P('p2', 'Generated', 4, 'generat|suppl')], 'c3'),
    ]

    cases = [{'id': 'k1', 'title': 'City Clinic', 'difficulty': 'moderate',
              'case': 'City Clinic has 40 beds; average occupancy 90% over 365 days. Annual ward costs: fixed ₹78,84,000, variable ₹500 per patient-day. It wants 25% profit on cost.',
              'mcqs': [
                  M('k1a', 'Patient-days:', ['13,140', '14,600', '12,000', '10,950'], 0,
                    '40 × 365 × 90% = 13,140. In practice: track daily census.', 'core', check=13140, topic=T3),
                  M('k1b', 'Fixed cost per patient-day:', ['₹600', '₹540', '₹500', '₹650'], 0,
                    '78,84,000 ÷ 13,140 = 600. In practice: rises if occupancy falls.', 'core', check=600, topic=T3),
                  M('k1c', 'Total cost per patient-day:', ['₹1,100', '₹1,000', '₹1,040', '₹600'], 0,
                    '600 fixed + 500 variable = 1,100. In practice: separate food and medicines.', 'core', check=1100, topic=T3),
                  M('k1d', 'Charge per patient-day:', ['₹1,375', '₹1,467', '₹1,320', '₹1,250'], 0,
                    '1,100 × 1.25 = 1,375. In practice: 25% on cost.', 'moderate', check=1375, topic=T3),
              ]}]

    return unit(UID, 'p4', 'int-p4-ch12', 1, 'Service Costing',
                ['Choose suitable cost units for services.',
                 'Compute transport costs using absolute and commercial tonne-km.',
                 'Cost and price hotel, hospital and other services.'],
                {'difficulty': 'core', 'minutes': {'learn': 25, 'practice': 35}, 'prereq': ['int-p4-ch11-u01'],
                 'exam_tip': 'Compute the service units (room-days, tonne-km) first; every rupee answer divides by them.'},
                concepts, [i1, i2], jobs, mcqs, questions,
                {'summary': ['Composite units: tonne-km, passenger-km, room-day, patient-day, kWh.',
                             'Absolute t-km = Σ load × distance; commercial = average load × total distance.',
                             'Standing, running and maintenance charges.',
                             'Hotels and hospitals: occupancy drives unit cost.'],
                 'remember': ['Profit on price: divide; on cost: multiply.'],
                 'traps': ['Ignoring occupancy overstates capacity.']},
                [('Absolute t-km', 'Σ load × distance'), ('Commercial t-km', 'Avg load × total km'), ('Room-days', 'Rooms × days × occupancy')],
                viva, cases)

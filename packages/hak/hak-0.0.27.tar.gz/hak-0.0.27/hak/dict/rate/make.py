from hak.string.print_and_return_false import f as pf
from hak.int.primes.prime_factors.get import f as get_prime_factors

# __init__
def f(numerator, divisor):
  if isinstance(numerator, dict):
    numerator = numerator['numerator']/numerator['divisor']

  if isinstance(numerator, float):
    decimal_place_count = len(str(numerator).split('.')[1].rstrip('0'))
    numerator *= 10**decimal_place_count
    divisor *= 10**decimal_place_count
    numerator = int(numerator)
    divisor = int(divisor)

  npf = get_prime_factors(numerator)
  dpf = get_prime_factors(divisor)

  common_factors = set(npf.keys()).intersection(set(dpf.keys()))

  while common_factors:
    common_factor = common_factors.pop()
    numerator //= common_factor
    divisor //= common_factor
    npf = get_prime_factors(numerator)
    dpf = get_prime_factors(divisor)
    common_factors = set(npf.keys()).intersection(set(dpf.keys()))

  return {'numerator': numerator, 'divisor': divisor}

def t_a():
  x = {'numerator': 10, 'divisor': 20}
  y = {'numerator': 1, 'divisor': 2}
  z = f(x['numerator'], x['divisor'])
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_b():
  x = {'numerator': 0.1, 'divisor': 0.2}
  y = {'numerator': 1, 'divisor': 2}
  z = f(x['numerator'], x['divisor'])
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_c():
  x = {'numerator': 100, 'divisor': 4}
  y = {'numerator': 25, 'divisor': 1}
  z = f(x['numerator'], x['divisor'])
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_d():
  x = {'numerator': 25.0, 'divisor': 1}
  y = {'numerator': 25, 'divisor': 1}
  z = f(x['numerator'], x['divisor'])
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_e():
  x = {'numerator': 80, 'divisor': 4}
  y = {'numerator': 20, 'divisor': 1}
  z = f(x['numerator'], x['divisor'])
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t_f():
  x = {'numerator': 0.7093094658085993, 'divisor': 1}
  y = {'numerator': 7093094658085993, 'divisor': 10**16}
  z = f(x['numerator'], x['divisor'])
  return y == z or pf([f"x: {x}", f"y: {y}", f"z: {z}"])

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_d(): return pf('!t_d')
  if not t_e(): return pf('!t_e')
  if not t_f(): return pf('!t_f')
  return True

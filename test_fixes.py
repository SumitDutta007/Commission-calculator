"""Quick test script to verify the fixes"""
import sys
sys.path.insert(0, 'backend')

from decimal import Decimal
from app.services.commission_service import CommissionCalculatorService

# Test boundary condition
service = CommissionCalculatorService()

# Test case 1: 79.99999% should NOT be eligible
sales1 = 95999.99
target1 = 120000.00
result1 = service.calculate_commission(sales1, target1)

print("Test 1: Boundary Condition (79.9999%)")
print(f"  Sales: ${sales1:,.2f}")
print(f"  Target: ${target1:,.2f}")
print(f"  Percentage: {result1.percentage_of_target:.10f}%")
print(f"  Eligible: {result1.eligible}")
print(f"  Commission: ${result1.commission:,.2f}")
print(f"  ✓ PASS" if not result1.eligible else "  ✗ FAIL")
print()

# Test case 2: Exactly 80% should be eligible  
sales2 = 96000.00
target2 = 120000.00
result2 = service.calculate_commission(sales2, target2)

print("Test 2: Exactly 80%")
print(f"  Sales: ${sales2:,.2f}")
print(f"  Target: ${target2:,.2f}")
print(f"  Percentage: {result2.percentage_of_target:.10f}%")
print(f"  Eligible: {result2.eligible}")
print(f"  Commission: ${result2.commission:,.2f}")
print(f"  ✓ PASS" if result2.eligible else "  ✗ FAIL")
print()

# Test case 3: 80.01% should be eligible
sales3 = 96012.00
target3 = 120000.00
result3 = service.calculate_commission(sales3, target3)

print("Test 3: Above 80% (80.01%)")
print(f"  Sales: ${sales3:,.2f}")
print(f"  Target: ${target3:,.2f}")
print(f"  Percentage: {result3.percentage_of_target:.10f}%")
print(f"  Eligible: {result3.eligible}")
print(f"  Commission: ${result3.commission:,.2f}")
print(f"  ✓ PASS" if result3.eligible else "  ✗ FAIL")

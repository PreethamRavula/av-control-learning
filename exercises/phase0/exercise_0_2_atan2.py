"""
Exercise 0.2: atan2 Practice

Master the angle-finding function used everywhere in robotics.

Your tasks:
    1. Implement angle_to_target()
    2. Implement angle_difference()
"""
import numpy as np
import matplotlib.pyplot as plt


def angle_to_target(robot_x, robot_y, target_x, target_y):
    """
    Calculate the angle FROM robot TO target in world frame.
    
    Args:
        robot_x, robot_y: Robot position
        target_x, target_y: Target position
    
    Returns:
        Angle in radians, range (-π, π]
    
    Example:
        Robot at (0,0), target at (1,1) → should return π/4 (45°)
        Robot at (0,0), target at (-1,0) → should return π (180°)
    
    Hint: np.arctan2(dy, dx) where dy = target_y - robot_y
    """
    # ============================================
    # YOUR CODE HERE (1 line)
    # ============================================
    dy = target_y - robot_y
    dx = target_x - robot_x
    angle = np.arctan2(dy, dx)  # TODO
    
    return angle


def angle_difference(target_angle, current_angle):
    """
    Calculate the smallest angle difference (how much to turn).
    
    This handles the wrap-around at ±π correctly.
    
    Args:
        target_angle: Where we want to face (radians)
        current_angle: Where we're currently facing (radians)
    
    Returns:
        Smallest signed angle to turn, range (-π, π]
        Positive = turn left (counterclockwise)
        Negative = turn right (clockwise)
    
    Examples:
        target=90°, current=0° → return +90° (turn left)
        target=-90°, current=0° → return -90° (turn right)
        target=170°, current=-170° → return -20° (NOT 340°!)
    
    Hint: After subtracting, use atan2(sin(diff), cos(diff)) to normalize
    """
    # ============================================
    # YOUR CODE HERE (2 lines)
    # ============================================
    diff = target_angle - current_angle  # TODO: target_angle - current_angle
    normalized = np.arctan2(np.sin(diff), np.cos(diff))  # TODO: normalize to (-π, π] using atan2
    
    return normalized


# ============================================
# TESTS - Don't modify below
# ============================================

def run_tests():
    print("="*50)
    print("Running Tests")
    print("="*50)
    
    all_passed = True
    
    # === angle_to_target tests ===
    print("\n--- angle_to_target tests ---")
    
    # Test 1: Target to the right (+X direction)
    result = angle_to_target(0, 0, 5, 0)
    expected = 0.0
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 1: Target at +X → 0°")
    else:
        print(f"✗ Test 1 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 2: Target above (+Y direction)
    result = angle_to_target(0, 0, 0, 5)
    expected = np.pi / 2
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 2: Target at +Y → 90°")
    else:
        print(f"✗ Test 2 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 3: Target to the left (-X direction)
    result = angle_to_target(0, 0, -5, 0)
    expected = np.pi
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 3: Target at -X → 180°")
    else:
        print(f"✗ Test 3 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 4: Target below (-Y direction)
    result = angle_to_target(0, 0, 0, -5)
    expected = -np.pi / 2
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 4: Target at -Y → -90°")
    else:
        print(f"✗ Test 4 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 5: Diagonal (Q1)
    result = angle_to_target(0, 0, 3, 3)
    expected = np.pi / 4
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 5: Target at (3,3) → 45°")
    else:
        print(f"✗ Test 5 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 6: Robot not at origin
    result = angle_to_target(2, 3, 5, 7)
    expected = np.arctan2(4, 3)  # dy=4, dx=3
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 6: Robot at (2,3), target at (5,7)")
    else:
        print(f"✗ Test 6 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # === angle_difference tests ===
    print("\n--- angle_difference tests ---")
    
    # Test 7: Simple difference
    result = angle_difference(np.radians(90), np.radians(0))
    expected = np.radians(90)
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 7: 90° - 0° = +90° (turn left)")
    else:
        print(f"✗ Test 7 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 8: Negative turn
    result = angle_difference(np.radians(-90), np.radians(0))
    expected = np.radians(-90)
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 8: -90° - 0° = -90° (turn right)")
    else:
        print(f"✗ Test 8 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 9: Wrap-around case (the tricky one!)
    result = angle_difference(np.radians(170), np.radians(-170))
    expected = np.radians(-20)  # Should turn right 20°, not left 340°!
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 9: 170° - (-170°) = -20° (wrap-around)")
    else:
        print(f"✗ Test 9 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    # Test 10: Another wrap-around
    result = angle_difference(np.radians(-170), np.radians(170))
    expected = np.radians(20)
    if result is not None and np.isclose(result, expected, atol=1e-10):
        print("✓ Test 10: -170° - 170° = +20° (wrap-around)")
    else:
        print(f"✗ Test 10 FAILED: expected {np.degrees(expected):.1f}°, got {np.degrees(result) if result else None}°")
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("Some tests failed. Keep trying!")
    print("="*50)
    
    return all_passed


def visualize():
    """Visualize angles to multiple targets"""
    robot_x, robot_y = 0, 0
    robot_theta = np.radians(30)  # Robot facing 30°
    
    targets = [
        (4, 0, "East"),
        (3, 3, "NE"),
        (0, 4, "North"),
        (-3, 3, "NW"),
        (-4, 0, "West"),
        (-3, -3, "SW"),
        (0, -4, "South"),
        (3, -3, "SE"),
    ]
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw robot
    ax.plot(robot_x, robot_y, 'bo', markersize=15, label='Robot')
    
    # Draw robot heading
    heading_len = 1.5
    ax.arrow(robot_x, robot_y, 
             heading_len * np.cos(robot_theta),
             heading_len * np.sin(robot_theta),
             head_width=0.2, head_length=0.15, fc='blue', ec='blue')
    ax.text(robot_x + 1.8*np.cos(robot_theta), 
            robot_y + 1.8*np.sin(robot_theta),
            f'Heading: {np.degrees(robot_theta):.0f}°', fontsize=10, color='blue')
    
    # Draw targets and angles
    for tx, ty, name in targets:
        # Draw target
        ax.plot(tx, ty, 'r*', markersize=15)
        
        # Calculate angle to target
        angle = angle_to_target(robot_x, robot_y, tx, ty)
        
        if angle is not None:
            # Calculate turn needed
            turn = angle_difference(angle, robot_theta)
            turn_deg = np.degrees(turn) if turn is not None else 0
            
            # Draw line to target
            ax.plot([robot_x, tx], [robot_y, ty], 'r--', alpha=0.3)
            
            # Label
            ax.text(tx + 0.3, ty + 0.3, 
                   f'{name}\nAngle: {np.degrees(angle):.0f}°\nTurn: {turn_deg:+.0f}°',
                   fontsize=9)
    
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Angles to Targets\n(Turn: + = left/CCW, - = right/CW)')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    passed = run_tests()
    if passed:
        print("\nShowing visualization...")
        visualize()
"""
Exercise 0.1: Rotation Matrix Transformation

Scenario:
    Your robot's LiDAR detects an obstacle at position (3, 0) in the SENSOR frame.
    (That means 3 meters directly ahead of the robot)
    
    The robot is at position (robot_x, robot_y) in the world, facing angle theta.
    
    Question: Where is the obstacle in WORLD coordinates?

Your task:
    Implement transform_to_world() function
"""
import numpy as np
import matplotlib.pyplot as plt


def transform_to_world(point_sensor, robot_x, robot_y, robot_theta):
    """
    Transform a point from robot/sensor frame to world frame.
    
    Args:
        point_sensor: np.array([x, y]) - Point in robot frame
        robot_x: Robot's X position in world
        robot_y: Robot's Y position in world  
        robot_theta: Robot's heading in world (radians)
    
    Returns:
        np.array([x, y]) - Point in world frame
    
    Steps:
        1. Build 2x2 rotation matrix for angle robot_theta
        2. Rotate the sensor point: rotated = R @ point_sensor
        3. Translate by robot position: world = rotated + [robot_x, robot_y]
    """
    # ============================================
    # YOUR CODE HERE
    # ============================================
    
    # Step 1: Build rotation matrix
    # R = [[cos(θ), -sin(θ)],
    #      [sin(θ),  cos(θ)]]
    c, s = np.cos(robot_theta), np.sin(robot_theta)
    R = np.array([[c, -s],
                  [s, c]])
    
    # Step 2: Rotate the point
    rotated = R @ point_sensor  # TODO
    
    # Step 3: Translate to world position
    point_world = rotated + [robot_x, robot_y]  # TODO
    
    return point_world
    # ============================================


def run_tests():
    """Test your implementation"""
    print("="*50)
    print("Running Tests")
    print("="*50)
    
    all_passed = True
    
    # Test 1: Robot at origin, facing +X (no rotation)
    result = transform_to_world(np.array([3.0, 0.0]), 0, 0, 0)
    expected = np.array([3.0, 0.0])
    if result is not None and np.allclose(result, expected):
        print("✓ Test 1: theta=0° (facing +X)")
    else:
        print(f"✗ Test 1 FAILED: expected {expected}, got {result}")
        all_passed = False
    
    # Test 2: Robot at origin, facing +Y (90° rotation)
    result = transform_to_world(np.array([3.0, 0.0]), 0, 0, np.pi/2)
    expected = np.array([0.0, 3.0])
    if result is not None and np.allclose(result, expected, atol=1e-10):
        print("✓ Test 2: theta=90° (facing +Y)")
    else:
        print(f"✗ Test 2 FAILED: expected {expected}, got {result}")
        all_passed = False
    
    # Test 3: Robot at (2, 1), facing +X
    result = transform_to_world(np.array([3.0, 0.0]), 2, 1, 0)
    expected = np.array([5.0, 1.0])
    if result is not None and np.allclose(result, expected):
        print("✓ Test 3: Robot at (2,1), theta=0°")
    else:
        print(f"✗ Test 3 FAILED: expected {expected}, got {result}")
        all_passed = False
    
    # Test 4: Robot facing backwards (180°)
    result = transform_to_world(np.array([3.0, 0.0]), 0, 0, np.pi)
    expected = np.array([-3.0, 0.0])
    if result is not None and np.allclose(result, expected, atol=1e-10):
        print("✓ Test 4: theta=180° (facing -X)")
    else:
        print(f"✗ Test 4 FAILED: expected {expected}, got {result}")
        all_passed = False
    
    # Test 5: Robot at (1,1), facing 45°, obstacle ahead and to the left
    result = transform_to_world(np.array([2.0, 1.0]), 1, 1, np.pi/4)
    # Expected: rotate (2,1) by 45°, then add (1,1)
    c, s = np.cos(np.pi/4), np.sin(np.pi/4)
    expected = np.array([2*c - 1*s + 1, 2*s + 1*c + 1])
    if result is not None and np.allclose(result, expected, atol=1e-10):
        print("✓ Test 5: theta=45°, offset obstacle")
    else:
        print(f"✗ Test 5 FAILED: expected {expected}, got {result}")
        all_passed = False
    
    print("="*50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("Some tests failed. Keep trying!")
    print("="*50)
    
    return all_passed


def visualize():
    """Visualize a transformation example"""
    # Setup: Robot at (2, 2), facing 60 degrees
    robot_x, robot_y = 2.0, 2.0
    robot_theta = np.radians(60)  # 60 degrees
    
    # Obstacle detected at (3, 0) in sensor frame (3m ahead)
    obstacle_sensor = np.array([3.0, 0.0])
    
    # Transform to world
    obstacle_world = transform_to_world(obstacle_sensor, robot_x, robot_y, robot_theta)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Draw world frame axes
    ax.arrow(0, 0, 1, 0, head_width=0.15, head_length=0.1, fc='gray', ec='gray')
    ax.arrow(0, 0, 0, 1, head_width=0.15, head_length=0.1, fc='gray', ec='gray')
    ax.text(1.2, 0, 'X_world', fontsize=10, color='gray')
    ax.text(0, 1.2, 'Y_world', fontsize=10, color='gray')
    
    # Draw robot as a triangle
    robot_size = 0.5
    robot_shape = np.array([
        [robot_size, 0],           # Nose
        [-robot_size/2, robot_size/2],   # Left rear
        [-robot_size/2, -robot_size/2],  # Right rear
        [robot_size, 0]            # Back to nose
    ])
    
    # Rotate robot shape
    c, s = np.cos(robot_theta), np.sin(robot_theta)
    R = np.array([[c, -s], [s, c]])
    rotated_shape = (R @ robot_shape.T).T + np.array([robot_x, robot_y])
    
    ax.fill(rotated_shape[:, 0], rotated_shape[:, 1], 'blue', alpha=0.6, label='Robot')
    ax.plot(robot_x, robot_y, 'bo', markersize=8)
    
    # Draw robot heading direction
    heading_length = 2
    ax.arrow(robot_x, robot_y, 
             heading_length * np.cos(robot_theta),
             heading_length * np.sin(robot_theta),
             head_width=0.2, head_length=0.15, fc='blue', ec='blue', alpha=0.5)
    
    # Draw obstacle
    if obstacle_world is not None:
        ax.plot(*obstacle_world, 'r*', markersize=20, label=f'Obstacle ({obstacle_world[0]:.1f}, {obstacle_world[1]:.1f})')
        
        # Draw line from robot to obstacle
        ax.plot([robot_x, obstacle_world[0]], [robot_y, obstacle_world[1]], 
                'r--', alpha=0.5, linewidth=2)
    
    # Labels and formatting
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 8)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    ax.set_title(f'Robot at ({robot_x}, {robot_y}), heading={np.degrees(robot_theta):.0f}°\n'
                 f'Obstacle: 3m ahead in sensor frame')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # First run tests
    passed = run_tests()
    
    # If tests pass, show visualization
    if passed:
        print("\nShowing visualization...")
        visualize()
    else:
        print("\nFix the tests first, then visualization will run!")
import java.util.*;

public class _001_TwoSum {
                                                                                                                                                                                    
    public int[] twoSum(int[] nums, int target) {                                                                                                                                 
        
        Map<Integer, Integer> seen = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {                                                                                                                                   
            int complement = target - nums[i];

            if (seen.containsKey(complement)) {                                                                                                                                   
                return new int[]{seen.get(complement), i};                                                                                                                        
            }                                                                                                                                                                     
            seen.put(nums[i], i);                                                                                                                                                 
        }                                                                                                                                                                         
        return new int[]{};                                                                                                                                                       
    }

    public static void main(String[] args) {
        _001_TwoSum solution = new _001_TwoSum();

        // Test case 1: [2,7,11,15], target=9 -> [0,1]
        int[] result1 = solution.twoSum(new int[]{2, 7, 11, 15}, 9);
        System.out.println("Test 1: " + Arrays.toString(result1));

        // Test case 2: [3,2,4], target=6 -> [1,2]
        int[] result2 = solution.twoSum(new int[]{3, 2, 4}, 6);
        System.out.println("Test 2: " + Arrays.toString(result2));

        // Test case 3: [3,3], target=6 -> [0,1]
        int[] result3 = solution.twoSum(new int[]{3, 3}, 6);
        System.out.println("Test 3: " + Arrays.toString(result3));
    }
}

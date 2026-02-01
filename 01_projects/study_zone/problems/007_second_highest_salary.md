## Second Highest Salary

**Difficulty:** Easy-Medium  
**Category:** SQL Aggregation / Subqueries

### Problem Statement

Write a SQL query to find the second highest salary from the `Employee` table. If there is no second highest salary (e.g., only one employee exists), return `NULL`.

### Schema

```sql
CREATE TABLE Employee (
    id INT PRIMARY KEY,
    salary INT NOT NULL
);
```

### Example

**Input:**

| id | salary |
|----|--------|
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |

**Output:**

| SecondHighestSalary |
|---------------------|
| 200                 |

**Input (Edge Case):**

| id | salary |
|----|--------|
| 1  | 100    |

**Output:**

| SecondHighestSalary |
|---------------------|
| NULL                |

### Constraints

- There may be duplicate salaries.
- The table may have zero, one, or many rows.
- Return exactly one row with column name `SecondHighestSalary`.

### Hints (only if stuck)

1. Consider using `DISTINCT` to handle duplicate salaries.
2. Think about `LIMIT` and `OFFSET`, or a subquery approach.
3. How can you ensure `NULL` is returned when no second highest exists?

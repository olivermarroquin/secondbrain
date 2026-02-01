
## 2026-02-01T04:08:07Z

**Tag:** joins

**Context:** problems/020_pwts_stub_test.md | playwright-ts/tests/020_pwts_stub_test.spec.ts

**Q:** Explain LEFT JOIN vs INNER JOIN with a tiny example.

**A:**

An `INNER JOIN` returns only the rows where the join condition is met in **both** tables.

A `LEFT JOIN` returns **all** rows from the left table, along with matching rows from the right table. If no match is found, columns from the right table will be `NULL`.

### Example

**Table `Employees`**
| ID | Name | DeptID |
|----|-------|--------|
| 1 | Alice | 101 |
| 2 | Bob | 102 |
| 3 | Charlie| NULL |

**Table `Departments`**
| ID | DeptName |
|----|----------|
| 101| Sales |
| 103| Engineering|

---

### INNER JOIN
`SELECT * FROM Employees INNER JOIN Departments ON Employees.DeptID = Departments.ID;`

**Result:** Only Alice is returned, as she's the only employee with a `DeptID` that exists in the `Departments` table.
| ID | Name | DeptID | ID | DeptName |
|----|-------|--------|----|----------|
| 1 | Alice | 101 | 101| Sales |

---

### LEFT JOIN
`SELECT * FROM Employees LEFT JOIN Departments ON Employees.DeptID = Departments.ID;`

**Result:** All employees are returned. Charlie, who has no department, has `NULL` for the department columns.
| ID | Name | DeptID | ID | DeptName |
|----|-------|--------|----|----------|
| 1 | Alice | 101 | 101| Sales |
| 2 | Bob | 102 | NULL| NULL |
| 3 | Charlie| NULL | NULL| NULL |

---

### Interview Angles

*   **Key Question:** "Show me all records from Table A, and if there's a match in Table B, show that too." This immediately signals a `LEFT JOIN`. "Show me only records that exist in both tables" signals an `INNER JOIN`.
*   **Finding Orphans:** A common use for `LEFT JOIN` is finding records in one table that have no corresponding record in another. The key is the `WHERE` clause:
    ```sql
    -- Find employees NOT in any valid department
    SELECT E.* FROM Employees E
    LEFT JOIN Departments D ON E.DeptID = D.ID
    WHERE D.ID IS NULL;
    ```
    This query would return Bob and Charlie.
*   **Symmetry:** `INNER JOIN` is symmetric (`A INNER JOIN B` is the same as `B INNER JOIN A`). `LEFT JOIN` is not. The order of the tables is critical.

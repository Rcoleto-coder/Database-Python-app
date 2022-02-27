-- 1.1 A list of product names.  Beside each product name, the category that product belongs to
select productname, CategoryName 
from Products
	join Categories	using(CategoryID) 
;


-- 1.2 A list of Order IDs, Order Dates, Company Names, and Countries for orders made by North American customers, sorted by order date
select orderid, orderdate, companyname, Country 
from orders
	join Customers on customers.CustomerID = orders.CustomerID 
where Country in ('Canada','Mexico','USA')
order by orderdate  
; 


-- 1.3 A list of DISTINCT names of suppliers that have products in the 'Seafood' category

select distinct companyname 
from Suppliers
	join Products using(SupplierID) 
		join Categories using(CategoryID) 
where products.CategoryID = 8
; 


-- 1.4.1 A list of Territory IDs and Descriptions.  For each row, show the ID of any Employee associated with the territory.
select territories.territoryid , territories.TerritoryDescription , employees.EmployeeID 
from territories 
	left join employeeterritories on employeeterritories.TerritoryID  = territories.TerritoryID 
		left join employees on employees.EmployeeID = employeeterritories.EmployeeID 
;


-- 1.4.2 A list of IDs and Descriptions of any territories that currently have NO associated employees
select territories.territoryid , territories.TerritoryDescription
from territories 
	left join employeeterritories on employeeterritories.TerritoryID  = territories.TerritoryID 
		left join employees on employees.EmployeeID = employeeterritories.EmployeeID 
where employees.EmployeeID is null
;


-- 1.4.3 A list of IDs, Descriptions, AND REGION NAMES of any territories that currently have NO associated employees
select territories.territoryid , territories.TerritoryDescription, regions.RegionDescription 
from territories 
	left join employeeterritories on employeeterritories.TerritoryID  = territories.TerritoryID 
		left join employees on employees.EmployeeID = employeeterritories.EmployeeID 
			left join regions on regions.RegionID = territories.RegionID  
where employees.EmployeeID is null
;


-- 1.5 A list of all possible combinations of Regions and Product Categories
select *
from regions cross join categories
;


-- 1.6.1 A list of Order IDs that shows the customer company name and employee name associated with that order
select OrderID , companyname , firstname, lastname
from orders
	join customers on customers.CustomerID = orders.CustomerID 
		join employees on employees.EmployeeID = orders.EmployeeID 
;


-- 1.6.2 Same as above, but include the name of each employee's immediate superior
select 
	OrderID,
	customers.companyname,
	employees.firstname,
	employees.lastname,
	boss.FirstName as BossFirstName,
	boss.LastName as BossLastName  
from orders
	join customers on customers.CustomerID = orders.CustomerID 
		join employees on employees.EmployeeID = orders.EmployeeID 
			join employees as boss on boss.EmployeeID = employees.ReportsTo 
;


-- 1.6.3 Same as above, but only show orders associated with employees who report to Steven Buchanan

select 
	OrderID,
	customers.companyname,
	employees.firstname,
	employees.lastname,
	boss.FirstName as BossFirstName,
	boss.LastName as BossLastName  
from orders
	join customers on customers.CustomerID = orders.CustomerID 
		join employees on employees.EmployeeID = orders.EmployeeID 
			join employees as boss on boss.EmployeeID = employees.ReportsTo 
where BossFirstName = 'Steven' and BossLastName = 'Buchanan'
;




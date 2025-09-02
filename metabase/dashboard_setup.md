# Metabase Dashboard Setup Guide

## Installation

1. **Download Metabase**
   ```bash
   # Download the JAR file
   wget https://downloads.metabase.com/v0.47.0/metabase.jar
   
   # Or use curl
   curl -O https://downloads.metabase.com/v0.47.0/metabase.jar
   ```

2. **Start Metabase**
   ```bash
   java -jar metabase.jar
   ```

3. **Access Metabase**
   - Open browser: http://localhost:3000
   - Complete initial setup wizard

## Database Connection

1. **Add MySQL Database**
   - Database type: MySQL
   - Host: localhost
   - Port: 3306
   - Database name: retail_warehouse
   - Username: root (or your MySQL username)
   - Password: [your_mysql_password]

2. **Test Connection**
   - Click "Test connection" to verify
   - Save the database connection

## Dashboard Components

### 1. Revenue Overview Dashboard

**Key Metrics Cards:**
- Total Revenue (from monthly_summary)
- Total Transactions (from transactions)
- Average Order Value (calculated)
- Unique Customers (from customers)

**Charts:**
- Monthly Revenue Trend (Line Chart)
- Revenue by Category (Bar Chart)
- Top 10 Customers (Table)
- Sales by Store Location (Bar Chart)

### 2. Customer Analytics Dashboard

**Charts:**
- Customer Segmentation (Pie Chart)
- Customer Lifetime Value Distribution (Histogram)
- Customer Retention by Month (Line Chart)
- Top Customers by Revenue (Table)

### 3. Product Performance Dashboard

**Charts:**
- Top Products by Revenue (Bar Chart)
- Category Performance (Donut Chart)
- Product Sales Trend (Line Chart)
- Inventory Turnover Analysis (Table)

### 4. Operational Dashboard

**Charts:**
- Daily Sales Pattern (Bar Chart)
- Payment Method Usage (Pie Chart)
- Store Performance Comparison (Table)
- Hourly Sales Distribution (Heatmap)

## Sample Questions for Metabase

### Revenue Analysis
```sql
-- Monthly Revenue Trend
SELECT year_month, total_revenue 
FROM monthly_summary 
ORDER BY year_month
```

### Customer Insights
```sql
-- Customer Segmentation
SELECT customer_segment, COUNT(*) as count, SUM(total_revenue) as revenue
FROM customers 
GROUP BY customer_segment
```

### Product Performance
```sql
-- Top Products by Revenue
SELECT product_name, category, total_revenue
FROM products 
ORDER BY total_revenue DESC 
LIMIT 10
```

### Store Analysis
```sql
-- Store Performance
SELECT store_location, COUNT(*) as transactions, SUM(revenue) as total_revenue
FROM transactions 
GROUP BY store_location 
ORDER BY total_revenue DESC
```

## Dashboard Filters

Set up the following filters for interactive dashboards:

1. **Date Range Filter**
   - Field: transaction_date
   - Type: Date range
   - Default: Last 30 days

2. **Category Filter**
   - Field: category
   - Type: Multi-select dropdown
   - Default: All categories

3. **Store Filter**
   - Field: store_location
   - Type: Multi-select dropdown
   - Default: All stores

4. **Customer Segment Filter**
   - Field: customer_segment
   - Type: Multi-select dropdown
   - Default: All segments

## Automated Reports

Configure email reports for:

1. **Daily Sales Summary**
   - Recipients: Management team
   - Schedule: Daily at 9 AM
   - Content: Key metrics and yesterday's performance

2. **Weekly Business Review**
   - Recipients: Stakeholders
   - Schedule: Monday mornings
   - Content: Weekly trends and insights

3. **Monthly Executive Report**
   - Recipients: Executive team
   - Schedule: First day of each month
   - Content: Monthly performance and KPIs

## Best Practices

1. **Performance Optimization**
   - Use database indexes for frequently queried fields
   - Limit large result sets with appropriate filters
   - Cache frequently accessed dashboards

2. **User Access Control**
   - Create user groups (Analysts, Managers, Executives)
   - Set appropriate permissions for each group
   - Restrict sensitive data access

3. **Dashboard Design**
   - Keep dashboards focused and uncluttered
   - Use consistent color schemes
   - Provide clear titles and descriptions
   - Add helpful tooltips and context

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Check MySQL is running
   - Verify network connectivity
   - Increase connection timeout settings

2. **Slow Query Performance**
   - Add database indexes
   - Optimize SQL queries
   - Use appropriate date ranges

3. **Memory Issues**
   - Increase Java heap size: `java -Xmx2g -jar metabase.jar`
   - Monitor system resources
   - Optimize dashboard queries

### Support Resources

- Metabase Documentation: https://www.metabase.com/docs/
- Community Forum: https://discourse.metabase.com/
- GitHub Issues: https://github.com/metabase/metabase/issues

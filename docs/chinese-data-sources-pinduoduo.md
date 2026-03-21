# Chinese Data Sources for Pinduoduo Analysis

Research completed: 2026-03-19

## Executive Summary

This document catalogs Chinese-language data sources available for analyzing Pinduoduo (拼多多), the domestic e-commerce platform operated by PDD Holdings. These sources represent what Chinese analysts, hedge funds, and researchers use to analyze Pinduoduo's business beyond US SEC filings.

**Key Finding**: China has a robust ecosystem of financial databases, consumer feedback platforms, market research firms, and app intelligence tools. However, many require paid subscriptions, and official platform GMV disclosure has declined since 2020-2021.

---

## 1. Financial Data Sources

### 1.1 Wind Information (万得)
- **URL**: https://www.wind.com.cn/
- **Description**: Leading Chinese financial data provider headquartered in Shanghai, offering comprehensive coverage of Chinese financial and securities data
- **Data Available**: Financial statements, market data, equity research, economic indicators
- **Access**: Paid subscription (terminal license)
- **Language**: Chinese (primary), some English
- **API**: Terminal-based, no public API
- **Notes**: Industry standard for institutional investors in China

### 1.2 CSMAR (China Stock Market & Accounting Research)
- **URL**: https://www.csmar.com/en/
- **Description**: Joint venture between GTA Information Technology, University of Hong Kong, and China Accounting and Finance Research Center
- **Data Available**: 4000+ variables from 200+ tables covering China stock markets and financial statements of listed companies
- **Access**: Institutional subscription (available through Wharton WRDS)
- **Language**: Chinese and English
- **API**: Database query interface
- **Coverage**: PDD Holdings financial data, peer company comparisons
- **Notes**: Widely used in academic research

### 1.3 iFinD (同花顺)
- **URL**: Operated by Hithink RoyalFlush Information Network
- **Description**: Chinese financial data terminal, competitor to Wind
- **Data Available**: Real-time market data, financial statements, research reports
- **Access**: Paid subscription
- **Language**: Chinese
- **Notes**: Previously involved in IP lawsuit with Wind

### 1.4 Choice Financial Terminal (东方财富)
- **Description**: Operated by Eastmoney, another major Chinese financial data provider
- **Data Available**: Market data, financial analysis tools
- **Access**: Paid subscription
- **Language**: Chinese

### 1.5 PDD Holdings SEC Filings vs. China Filings
- **CSRC (China Securities Regulatory Commission)**: PDD has taken position they don't require CSRC permission for offshore offerings (per legal counsel). However, future capital market activities may require CSRC filing per Trial Administrative Measures (effective March 31, 2023)
- **SAMR (State Administration for Market Regulation)**: No mandatory antitrust filings found for PDD beyond normal M&A thresholds
- **Conclusion**: Limited additional financial disclosure in China beyond US SEC filings

---

## 2. Consumer/Merchant Feedback Platforms

### 2.1 黑猫投诉 (Heimao Tousu / Black Cat Complaints)
- **URL**: https://tousu.sina.com.cn
- **Pinduoduo Page**: https://tousu.sina.com.cn/company/view?couid=1003609
- **Operator**: Sina (新浪)
- **Description**: Major consumer complaint platform in China

**Data Available**:
- Individual consumer complaints against Pinduoduo (searchable database)
- Complaint volume rankings (Pinduoduo consistently in top 3 e-commerce platforms)
- Response rate metrics (Pinduoduo showed improved response rates in 2024)
- Common complaint categories (customer service, refunds, false shipping)

**Metrics** (from December 2025 report):
- Pinduoduo ranked in top 3 e-commerce platforms by complaint volume
- Also appeared on November "black list" for poor complaint handling
- Response times for typical cases: ~2 hours

**Access**: Free, web scraping possible
**API**: No official API, but scraping tutorial exists: https://textdata.cn/blog/2025-03-05-scrape-consumer-complaint-data-with-python/
**Data Quality**: Real consumer complaints with merchant/platform responses
**Language**: Chinese only

### 2.2 12315 Government Consumer Complaint Platform
- **URL**: https://12315.cn
- **Hotline**: 12315 (nationwide)
- **Operator**: State Administration for Market Regulation (国家市场监督管理总局)
- **Description**: Official government consumer protection platform

**Data Available**:
- Consumer complaints filed against Shanghai Xunmeng Information Technology Co., Ltd. (上海寻梦信息技术有限公司 - Pinduoduo's legal entity)
- Complaint resolution data
- Success rates by year

**Effectiveness** (2023-2024 data):
- 67% of Pinduoduo dispute cases resolved through 12315 in 2023
- Success rate increased from 51% (2020) to 65% (2024)
- Mandatory binding power over Pinduoduo

**Access**: Free, online filing at https://12315.cn or via WeChat official account
**API**: No public API
**Data Quality**: Official government-mediated complaints
**Language**: Chinese only

### 2.3 知乎 (Zhihu)
- **URL**: https://www.zhihu.com
- **Pinduoduo Topics**: Search "拼多多商家" or "拼多多卖家"
- **Description**: Chinese Q&A platform (similar to Quora)

**Data Available**:
- Merchant/seller discussions and experiences
- Operational guides (virtual products, stock management, customer service metrics)
- Business model analysis
- Temu cross-border discussions
- Consumer perspectives and reviews

**Notable Topics**:
- Selling on Pinduoduo: registration, operations, commission rates
- Platform policies: "百亿减免" (10 billion yuan promotion fee reduction)
- Merchant pain points: stock shortages, refund policies, brand authorization
- Commission rate evolution: 1.24% (2017) → 2.99% (current), still lower than JD/Alibaba

**Access**: Free browsing, requires account for full access
**API**: No official API
**Scraping**: Possible but requires anti-bot measures
**Language**: Chinese only

### 2.4 小红书 (Xiaohongshu / RED / RedNote)
- **URL**: https://www.xiaohongshu.com
- **Description**: Lifestyle and e-commerce social platform

**User Demographics**:
- 350 million MAU (Monthly Active Users)
- 70% born after 1990
- ~70% female
- 50% from Tier 1-2 cities
- Users open app avg. 16 times/day
- 9 million notes posted daily, 70 million comments

**Pinduoduo-Related Data**:
- Consumer reviews and shopping experiences
- Merchant perspectives on selling strategies
- Product discovery and purchase intentions
- Note: Xiaohongshu skews premium/urban vs. Pinduoduo's value/rural positioning

**Access**: Free browsing, requires account for full access
**API**: No public API
**Data Quality**: UGC (90% user-generated content), high engagement
**Language**: Chinese only

### 2.5 Merchant Forums & Communities

**Official Pinduoduo Resources**:
- **多多大学 / 拼多多课堂 (Pinduoduo Classroom)**: Official merchant training platform within Pinduoduo app
  - Content: Operations, marketing strategies, product selection, store management, customer service
  - Access: Free, within Pinduoduo merchant backend
  - Format: Online courses, articles, videos, case studies

**Third-Party Merchant Communities**:
- **学买卖 (Xuemaimai)**: https://xuemaimai.com/forum-278-207.html
  - "Pinduoduo Seller Circle" created Sept 2022
  - 6,000+ posts, 5 million+ views

- **店托易 (Diantuoyi)**: https://diantuoyi.com/circle/pinduoduo
  - Pinduoduo merchant exchange community

**Note**: Unlike Amazon's robust seller forums, Pinduoduo lacks official forum. Most merchant discussions occur on third-party platforms.

---

## 3. Market Research Firms

### 3.1 QuestMobile (贵士信息)
- **URL**: https://www.questmobile.com.cn/
- **Founded**: 2014 (founder: Zhou Yucheng)
- **Focus**: Mobile internet big data, data visualization, app usage analytics

**Data Available**:
- App usage data (MAU, DAU, session time)
- User demographics and behavior
- Industry reports on mobile e-commerce
- Competitive landscape analysis

**Pinduoduo Coverage**: Yes, as major Chinese e-commerce app
**Access**: Reports available (many require payment)
**API**: No public API
**Language**: Chinese primarily

### 3.2 iResearch (艾瑞咨询)
- **Founded**: 2002
- **Description**: Earliest third-party organization involved in Chinese internet research

**Data Available**:
- Internet consulting services with data support
- E-commerce market reports
- User behavior studies
- Platform comparisons

**Access**: Free reports (limited) + paid subscription for detailed reports
**Language**: Chinese primarily
**Notes**: Established player with historical data dating to early 2000s

### 3.3 Analysys (易观)
- **URL**: https://www.analysys.cn/
- **Founded**: 2000 (Beijing subsidiary 2012)
- **Focus**: Big data analysis and consulting

**Data Available**:
- Mobile app analytics
- E-commerce market sizing
- Consumer insights
- Platform performance metrics

**Reports**: https://www.analysys.cn/article/analysis/
**Access**: Free and paid reports
**Language**: Chinese primarily

### 3.4 iiMedia Research (艾媒咨询)
- **URL**: https://www.iimedia.cn/
- **Reports**: https://report.iimedia.cn/
- **Description**: New economy industry data analysis and reporting

**Recent Pinduoduo Coverage** (2025-2026):
- "2025 China Brand E-commerce Service Provider Industry Research Report"
  - Analyzes Pinduoduo's cost structure (2023-2024)
  - Low-price positioning, merchant cost reduction
  - Lower-tier market consolidation
  - Temu overseas expansion

- "2025 China E-commerce 'Double Eleven' Consumer Big Data Monitoring Report"
  - Top 3 platforms: Taobao/Tmall, JD.com, Pinduoduo

- "2025-2026 China Lower-Tier Market Instant Delivery Platform Trend Insight Report"

**Market Size Data** (from 2025 reports):
- Brand e-commerce service industry: 446.85 billion yuan (2024), +9.6% YoY
- Projected to exceed 586.23 billion yuan by 2028

**Access**: Free summaries, paid full reports
**Language**: Chinese primarily

### 3.5 Industry Usage Notes
- These four firms (QuestMobile, iResearch, Analysys, iiMedia) are commonly used together for comprehensive China internet market research
- Data breadth/accuracy ranking (per Chinese analysts): App Annie > Sensor Tower for China market
- Reports often require payment for detailed data tables and full analysis

---

## 4. App Intelligence & Traffic Data

### 4.1 七麦数据 (Qimai Data)
- **URL**: https://www.qimai.cn/
- **App**: iOS App Store (七麦数据)
- **Description**: Professional mobile app data analysis platform for Chinese market

**Coverage**:
- 155 countries/regions
- App Store & Google Play
- 9 major Chinese Android app markets

**Metrics Available**:
- App Store rankings (real-time)
- Download estimates
- Revenue estimates
- ASO (App Store Optimization) data
- DAU/MAU estimates
- Retention rates
- Crash rates
- Search index
- WeChat official account rankings

**Access**: Free tier (limited) + paid subscription
**API**: Web-based dashboard
**Language**: Chinese
**Update Frequency**: Real-time
**Notes**: Most comprehensive for Chinese app market

### 4.2 App Annie (data.ai)
- **Description**: Global mobile data and analytics
- **China Coverage**: Broad, considered most accurate for China market
- **Data Available**: Downloads, MAU/DAU, revenue, market share
- **Access**: Paid subscription (enterprise-level)
- **Comparison**: Generally broader data coverage than Sensor Tower for China

### 4.3 Sensor Tower
- **URL**: https://sensortower.com/
- **Description**: Digital intelligence & app data analysis
- **China Coverage**: Good, but slightly less comprehensive than App Annie per Chinese analysts
- **Data Available**: App performance metrics, market intelligence
- **Access**: Paid subscription

### 4.4 Recent Pinduoduo App Data (2026)
- **Market Position**: Pinduoduo was the most used e-commerce app in China (per Business of Apps, 2026)
- **Note**: Alibaba had most users when combining Taobao + Tmall, but Pinduoduo led as single app
- **Source**: Multiple market research reports

---

## 5. Logistics & Delivery Data

### 5.1 Major Chinese Delivery Companies

**The Big Players**:
1. **SF Express (顺丰)** - Premium delivery
2. **ZTO Express (中通)** - Market leader by volume
3. **YTO Express (圆通)** - Major player
4. **Yunda Express (韵达)** - Growing rapidly
5. **STO Express (申通)** - "通达系" network
6. **Best Express (百世)** - Struggling
7. **J&T Express (极兔)** - Fast-growing newcomer

### 5.2 Available Volume Data (H1 2024 - Most Recent)

**Business Volume**:
- ZTO: 15.623 billion parcels (+11.8% YoY)
- YTO: 12.204 billion parcels (+24.8% YoY)
- Yunda: 10.924 billion parcels (+30.0% YoY)
- STO: 10.227 billion parcels (+32.5% YoY)
- SF Express: 6.214 billion parcels (+6.5% YoY)

**Market Share** (2024):
- ZTO: 19.4%
- YTO: 15.2%
- Yunda: 13.6%
- STO: 12.8%
- J&T: 11.0%
- SF Express: 7.75%

**2025 Industry Overview**:
- First 11 months of 2025: 180.74 billion parcels (+14.9% YoY)
- Monthly average: >16 billion parcels
- Q1-Q3 2025: ZTO/YTO/STO/Yunda handled 280/226/189/191 billion parcels (growth +14.8%/+19.4%/+17.1%/+13.0%)

### 5.3 Pinduoduo Correlation
**Critical Gap**: Search results did NOT find specific data correlating these delivery companies' volumes with Pinduoduo GMV.

**Potential Sources**:
- Company earnings calls (ZTO, YTO, etc. may discuss e-commerce platform partnerships)
- Industry reports mentioning platform-specific delivery partnerships
- Investor presentations

**Notes**: This would be a valuable data mining target - estimating Pinduoduo GMV from delivery partner volume data.

---

## 6. Government & Industry Reports

### 6.1 Ministry of Commerce (商务部)
- **URL**: https://dzswgf.mofcom.gov.cn/
- **Reports Portal**: https://dzswgf.mofcom.gov.cn/m_yjbg/page1.html

**Available Reports**:
- "中国电子商务报告" (China E-Commerce Report) - Annual comprehensive report
- "2024年上半年我国电子商务发展情况" (H1 2024 E-commerce Development)
- "2025年1-6月我国电子商务发展情况" (Jan-Jun 2025 E-commerce Development)

**Data Available**:
- National e-commerce GMV
- Market size and growth rates
- Platform ecosystem analysis
- Cross-border e-commerce data
- Rural e-commerce development

**Access**: Free download (PDF reports)
**Language**: Chinese (official reports), some English summaries
**API**: No API, manual download only

### 6.2 National Bureau of Statistics (国家统计局)
- **URL**: http://www.stats.gov.cn/

**Recent Data** (March 2026):
- Retail sales of consumer goods: +2.8% YoY (Jan-Feb 2026)
- Published through Ministry of Commerce as well

**E-commerce Specific Data**: Limited granularity by platform
**Access**: Free, official government statistics
**Language**: Chinese and English

### 6.3 CNNIC (China Internet Network Information Center)
- **Report**: "Statistical Report on China's Internet Development"
- **Description**: Comprehensive internet usage statistics used by market researchers
- **Data Available**: Internet penetration, user demographics, e-commerce adoption
- **Access**: Free download
- **Language**: Chinese and English

### 6.4 Market Size Data (2026)
From various government and research reports:
- China e-commerce market: Expected to reach $1.14 trillion (2026)
- Projected growth to $2.52 trillion by 2030 (10.42% CAGR)
- Monthly revenues (Feb 2026): $149.85 billion
- Historical: $3 trillion (2015) → $6.5 trillion (2024)

**Platform Rankings by GMV** (2025 data):
1. Pinduoduo: $780.45 billion
2. TikTok Shop: (Second place)
3. Taobao: (Third place)

**Note**: Major platforms (Tmall, JD, Pinduoduo) stopped disclosing platform GMV since 2020-2021, making third-party estimates critical.

---

## 7. Pricing & Product Data

### 7.1 Pinduoduo Official Open Platform
- **URL**: https://open.pinduoduo.com/
- **API Gateway**: https://gw-api.pinduoduo.com/api/router
- **OAuth**: https://open-api.pinduoduo.com/oauth/token

**Authentication**:
- Requires `client_id` and `client_secret`
- OAuth 2.0 authorization flow
- Multiple member types: MERCHANT, H5, JINBAO (多多进宝), KTT (快团团), LOGISTICS

**API Capabilities**:
- Product listings and details
- Order management
- Logistics tracking
- Marketing data
- Inventory management

**Limitations**:
- Rate limits apply
- Access tokens expire (require refresh)
- Some interfaces require merchant store authorization
- Designed for merchants/partners, not public data access

**Developer Resources**:
- GitHub SDKs: https://github.com/justmd5/pinduoduo-sdk, https://github.com/zhuger/pinduoduo, https://github.com/jubull/pinduoduo

### 7.2 Third-Party Data Providers

**TMAPI (Professional E-Commerce API Provider)**:
- **URL**: https://tmapi.top/
- **Service**: Historical price trends API
- **Platforms**: Pinduoduo, Taobao, Tmall, JD.com, vip.com
- **Data**: Price history by product ID
- **Access**: Paid API service

**慢慢买 (Manmanbuy)**:
- **Description**: E-commerce price comparison platform with 10+ years data collection
- **Coverage**: Major Chinese e-commerce platforms
- **Service**: Cross-platform price comparison API
- **Access**: Paid

**订单侠 (Dingdanxia)**:
- **URL**: https://www.dingdanxia.com/doc/216/86
- **Service**: Pinduoduo product detail API
- **Data**: Title, description, group-buy price, single-buy price, coupons, ratings, commission rates
- **Access**: Paid API

### 7.3 Scraping Services

Multiple commercial providers offer Pinduoduo scraping:
- **Bright Data**: https://brightdata.com/products/web-scraper/pinduoduo
  - Pinduoduo Price Tracker
  - Real-time pricing updates
  - Historical trend analysis

- **iWebDataScraping**: Pinduoduo Product Data Scraping API
- **Actowiz Solutions**: Extract Pinduoduo API Product Data
- **RetailScrape**: Real-time product insights

**Technical Challenge**: Pinduoduo mobile site (mobile.yangkeduo.com) requires phone number + SMS verification for every page (search, product detail, categories)

**Data Points Available**: Title, seller name, brand, description, initial price, currency, availability, reviews count, images, specifications

### 7.4 Price Intelligence Use Cases
- Cross-platform price comparison apps
- Merchant competitive pricing analysis
- Sales trend prediction
- Dynamic pricing optimization
- Consumer shopping assistance tools

---

## 8. Summary Matrix

| Category | Best Sources | Free/Paid | API | Scraping | Language |
|----------|-------------|-----------|-----|----------|----------|
| **Financial Data** | Wind, CSMAR | Paid | Terminal | No | CN/EN |
| **Consumer Complaints** | 黑猫投诉, 12315 | Free | No | Yes | CN |
| **Social Discussions** | Zhihu, Xiaohongshu | Free | No | Limited | CN |
| **Market Research** | QuestMobile, iResearch, Analysys, iiMedia | Free+Paid | No | No | CN |
| **App Intelligence** | 七麦数据, App Annie, Sensor Tower | Paid | Dashboard | No | CN/EN |
| **Logistics Data** | Company earnings, industry reports | Free+Paid | No | No | CN/EN |
| **Government Data** | MOFCOM, NBS, CNNIC | Free | No | No | CN/EN |
| **Product/Price Data** | Third-party APIs, scraping services | Paid | Yes | Yes | CN/EN |

---

## 9. Data Gaps & Opportunities

### 9.1 Critical Gaps Identified
1. **Logistics Correlation**: No public data linking delivery company volumes to specific e-commerce platforms (especially Pinduoduo)
2. **Platform GMV**: Major platforms stopped disclosing GMV in 2020-2021
3. **Real-time Pricing**: Pinduoduo SMS verification makes large-scale scraping difficult
4. **Merchant Economics**: Limited public data on merchant profitability, commission impact

### 9.2 High-Value Data Sources
1. **黑猫投诉** (Heimao Tousu): Scrapable, real consumer sentiment, competitive benchmarking
2. **七麦数据** (Qimai): Real-time app rankings, download/revenue estimates
3. **Third-party Price APIs**: Historical pricing trends for competitive analysis
4. **Ministry of Commerce Reports**: Official market sizing and growth rates
5. **Zhihu Merchant Discussions**: Qualitative insights into platform changes, merchant pain points

### 9.3 Recommended Data Mining Priorities

**Tier 1 - Implement Now**:
- 黑猫投诉 scraper (consumer complaints analysis)
- Ministry of Commerce report parser (official market data)
- 七麦数据 integration (app intelligence)
- Zhihu discussion monitor (merchant sentiment)

**Tier 2 - High Value if Budget Allows**:
- Third-party price API integration (TMAPI or similar)
- QuestMobile/iResearch report subscriptions (market research)
- CSMAR access (financial peer analysis)

**Tier 3 - Experimental**:
- Pinduoduo product scraping (SMS verification challenge)
- Xiaohongshu consumer sentiment analysis
- Logistics volume correlation modeling

---

## 10. Sources

### Financial Data
- [CSMAR DATA](https://www.csmar.com/en/)
- [Wind Information - Wikipedia](https://en.wikipedia.org/wiki/Wind_Information)
- [CSRC's New Requirements for Overseas Listings](https://www.nortonrosefulbright.com/en/knowledge/publications/b67e7590/csrcs-new-requirements-for-overseas-listings-by-prc-domestic-companies)
- [PDD Holdings 2022 Annual Report](https://www.annualreports.com/HostedData/AnnualReportArchive/p/NASDAQ_PDD_2022.pdf)

### Consumer Complaints
- [拼多多_黑猫投诉](https://tousu.sina.com.cn/company/view?couid=1003609)
- [黑猫投诉数据采集教程](https://textdata.cn/blog/2025-03-05-scrape-consumer-complaint-data-with-python/)
- [怎么在12315平台上投诉拼多多卖家](https://www.zhihu.com/question/411541855)
- [12315投诉拼多多有用吗](https://www.021van.com/news/70979.html)

### Social Platforms
- [在拼多多中售卖虚拟物品的详细过程](https://zhuanlan.zhihu.com/p/1909280195816449174)
- [拼多多业务模式理解及启示](https://zhuanlan.zhihu.com/p/148063095)
- [2024 REDNote (Xiaohongshu) Marketing Guide](https://walkthechat.com/xiaohongshu-little-red-book-fostering-e-commerce-via-word-mouth/)
- [Xiaohongshu - Wikipedia](https://en.wikipedia.org/wiki/Xiaohongshu)

### Market Research
- [QuestMobile](https://www.questmobile.com.cn/)
- [易观分析](https://www.analysys.cn/)
- [艾媒咨询](https://www.iimedia.cn/)
- [艾媒咨询 | 2025年中国品牌电商服务商行业研究报告](https://www.iimedia.cn/c400/106565.html)

### App Intelligence
- [七麦数据](https://www.qimai.cn/)
- [Sensor Tower](https://sensortower.com/)
- [有没有什么工具可以查App的日活](https://www.zhihu.com/question/39138785)

### Logistics
- [2026快递开启新角逐](https://finance.sina.com.cn/stock/relnews/cn/2025-12-22/doc-inhcsmfe9176443.shtml)
- [快递2025：谁在股价狂欢](https://iot.ofweek.com/2026-01/ART-132200-12003-30678343.html)

### Government Data
- [中国电子商务报告](https://opendata.mofcom.gov.cn/front/data/detail?id=B81C4D46AF081F881468B4E0E4830E20)
- [China's retail sales up 2.8% in first two months](https://www.ecns.cn/china/2026-03-17/detail-ihfaunkv7710582.shtml)
- [China Shopping App Revenue and Usage Statistics (2026)](https://www.businessofapps.com/data/china-ecommerce-market/)

### Pricing & Product Data
- [Pinduoduo API and dropshipping](https://otcommerce.com/pinduoduo-api-dropshipping/)
- [个人开发者接入拼多多开放平台](https://zhuanlan.zhihu.com/p/1986726961444311993)
- [TMAPI Price Comparison API](https://tmapi.top/docs/price-comparison/historical-price-cn/get-item-historical-price-by-id/)
- [Pinduoduo Price Tracker - Bright Data](https://brightdata.com/products/insights/price-tracker/pinduoduo)
- [拼多多商品详情接口 - 订单侠](https://www.dingdanxia.com/doc/216/86)

### Merchant Communities
- [多多大学：拼多多为卖家提供的电商培训和教育平台](https://zhuanlan.zhihu.com/p/640216881)
- [拼多多卖家圈 - 学买卖](https://xuemaimai.com/forum-278-207.html)
- [拼多多商家交流社区论坛圈子 – 店托易](https://diantuoyi.com/circle/pinduoduo)

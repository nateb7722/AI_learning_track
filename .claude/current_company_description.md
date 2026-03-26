

Double Good is a virtual fundraising company. We make gourmet popcorn in-house and sell it via fundraisers, sharing the revenue 50/50 with the people running the fundraiser

How it works:

- Each fundraiser requires an organizer. This person is the one who physically creates the fundraising event on our platform, schedules it, and gives us some information related to what the fundraising is for. This is also the person who will receive the 50% of revenue.

- Once the organizer creates and plans the event, they need to recruit sellers for the event. These sellers receive a code for the event or a link to sign up as a seller. After enrolling in the event, they create a virtual store, and add a picture and a description about what they are fundraising for. The organizer can act as a seller as well.

- Each fundraiser lasts 4 days, which means sellers usually have to create and set up their store before the fundraiser starts and participants need to act rather quickly. However, the company has very recently decided to change this. They are now allowing 2 days of pre-sales to early visitors and will soon also add 2 days of post-sales for late viewers. Later on, they will also create a 7-day option in addition to the standard 4 day


How fundraisers sell:

- The sellers are primarily responsible for finding buyers to buy from their store. They usually send text messages to friends and family as well as post on social media sites. We have a button on the store page for sellers to share with templates and such for instagram, facebook, etc. We believe sellers primarily click that button, copy the link, and send it via text messages. Buyers can also visit a store and choose to share. We see in many cases friends and family will also get the link, either from the store page or directly from the seller, and posting on social media on their behalf.

- Given that the “marketing” for the event and its stores is only happening from those involved in the event, or directly connected to someone in the event, this means we are basically leveraging local networks. We are not leveraging a “network effect” by trying to connect all of the people in our system to buyers or fundraisers that might find a mutual benefit. This means we run the risk of market “over saturation” with too many events or stores happening in the same place, if they are all trying to tap the same pool of buyers.

The popcorn:

- The popcorn is made fresh and sent out within a week or two. We have many different flavors from caramel to different spicy cheeses, with engaging branding. Buyers usually love the popcorn, but think it's expensive. We also offer “sets” that are multi-bag combinations that are sold at a discount to what the price would be if they were bought individually. This is also a frequently bought item due to the simplicity and cheaper price. Buyers mostly buy to support the seller and fundraiser, and care less about the popcorn. Often buyers will buy a  “donation” purchase, where 50% still goes to the seller, but the popcorn they would have received will now be donated to first responders or another good cause. Once the buyer purchases the popcorn, the seller is notified and can send a thank you through the app. We send the popcorn directly to the buyer and handle all of the shipping and communication for the seller.

Terminology:

- The fundraiser is often called an “event” at our company. The total revenue is called “gross sales” and dividing the gross sales by 2 is how we arrive at “net sales”. This is because we split the revenue 50/50.  Identifiers for the fundraiser are fundraiser_uuid and event_code.

- When a seller runs their store for an event, it is called a “campaign”. If they participate as a seller later on for a different event, they simply update their store. They are not creating a new store. That is why the campaign is the unique combination of fundraiser and store. 


Key Markets:

- When the app was first created, the biggest users were cheerleading teams. After the pandemic, the “divine 9” fraternities and sororities were a big driver of our growth. Their fundraisers from 2021 are still some of the biggest we have ever had. We now operate  in the youth sports market - little league baseball teams, basketball teams, etc. In these cases the organizer is usually the coach, and the sellers are the kids, or the parents of the kids. They fundraiser for equipment, travel costs to tournaments etc.

- We also operate in the high school sports and activities space. Sports teams, clubs, band etc. Similarly, the organizer is usually the coach or teacher of the group, and the students are the sellers.

- Another area is the religious organization space. They often run a high number of events, but they are smaller and not as profitable. This is usually for a church or other religious or charitable cause.

- We also support school fundraisers. These are usually elementary or junior high schools. The organizer is usually the principal or another high level administrator. The sellers are usually the kids, parents, and/or teachers. These are usually very large events

- Current level of analytics and key drivers the company is interested in: 

- The company is currently very focused on what they call the “flywheel”. This is the organic growth that occurs from buyers or sellers converting to an organizer at a later date. Many users first hear about Double Good due to someone they know running a fundraiser. They purchase to support the cause, they enjoy the popcorn, and then end up organizing themselves later on. There is an additional big focus on “large events” that are expected to raise over $6,000. These are usually school level fundraisers, as they have the most sellers. 

- For the past year or so, the company has been investing more in paid advertising. Primarily through google. It seems to be bringing in business, although these events are less likely to actually have sales, and when they do it is often smaller. 

- The company is also interested in retention, but given the multiple roles available, it is a complex topic that has not been aligned on.

Important notes for key metrics:

- Fundraiser sales (also called event sales):
    - The distribution for our fundraiser sales is non-normal with an extreme right skew.
  When log transforming, it becomes normal, but there is a bi-modal distribution. This is because roughly 30% of our events are “single seller” meaning the organizer is the only seller. This is fundamentally different from the rest of our events and the type of event we try to support

- Campaign sales:
    - This is also severely skewed with a similar extreme right skew
  When log transforming, it becomes normal, but there is a multi-modal distribution. There is a massive second peak on the left tail, and that is because of campaigns that only had one buyer who bought roughly the minimum purchase. I have not dug into this enough yet, but it is likely these buyers are often the seller themselves. There is a second peak slightly higher than the normal bell curve peak but I have not found out why yet.

- Retention:
    - Organizers most commonly run one event a year if we successfully retain them. However, it is possible they buy or sell within that time
  Given organizers usually run one event a year, the sellers for their cause are often also on a yearly retention schedule (if we are successful in retaining them).
  For buyers that only know of one seller or cause that fundraisers, and they do so every year, they might also only purchase yearly

Fundraiser Activation:

 - Many fundraisers are scheduled, often just to test out the app, but don’t have any sales. This is mostly users who did not actually intend to sell anything, and were just interested in seeing what the app is. 
Fundraiser Activation can be looked at by viewing the percent of events that are finished that did not have any sales

Seller Activation:
 - For many events, there are sellers who sign up but then don’t make any sales. In many cases it is because they don’t actually intend to. For example, a high school team may run a fundraiser where the coach is the organizer, and tells the players they have to make a store. Some kids don’t really care, so they make the store but then don’t actually send the link to anyone or try to sell the popcorn.
One way this can be looked at is comparing total_sellers with active_sellers on the events360 dataset

Key datasets:
 - For events, we can use the data_warehouse.core.events360 dataset. The primary key is fundraiser_uuid. It has information on the number of total sellers, active sellers, taxonomy and location information, sales information, etc.
 - For orders we can use the data_warehouse.core.order transactions dataset. The primary key is order_transactions_id. It has order_number as well, which is mostly unique, but sometimes duplicated if a user added a donation purchase to their order. It has information on the amounts, status, channel, order date, and ship date. The channel we are mostly interested in is “Virtual Fundraising”. That is the channel where buyers buy from the campaign
 - For holistic user information we can use the customer360 models. DATA_WAREHOUSE.CORE.COMBINED_USER_INFO_CUSTOMER360 has information on organizing, selling, and buying activities for any user who has sold or organized. Key features include start and end dates for first activities, last activities, “path” which is a string explaining their first activities and subsequent conversions. It includes the days for converting between different roles, total sales and purchases, etc. This is unique by standardized email ( upper(trim(email))). Other similar datasets are DATA_WAREHOUSE.CORE.seller_information_customer360, DATA_WAREHOUSE.CORE.organizer_information_customer360, DATA_WAREHOUSE.CORE.buyer_information_customer360
 - For an easy list of actions a user has taken, the DATA_WAREHOUSE.CORE.all_actions_customer360 dataset has a list of actions and their date for a standardized email. The action_uuid column links to fundraiser_uuid, campaign_uuid, or order_transaction_id

@pytest.fixture()
def setup():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://magento.softwaretestingboard.com/")
    driver.implicitly_wait(5)
    driver.maximize_window()
    yield driver
    driver.close()

    time.sleep(5)


test_fn_sign_up_gmail_yahoo = [
    ["Aviram", "Cohen", "examplez1@yahoo.com", "Acccccs1230"],
    ["Moshe", "Rubinstein", "examplez2@gmail.com", "Bccccs1230"]
]


@pytest.mark.parametrize("users", test_fn_sign_up_gmail_yahoo)
def test_fn_sign_up_gmail_and_yahoo(setup, users):
    driver = setup

    driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/ul/li[3]/a').click()
    webdriver.support.ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstname")))
    driver.find_element(By.ID, "firstname").send_keys(users[0])
    driver.find_element(By.ID, "lastname").send_keys(users[1])
    driver.find_element(By.ID, "email_address").send_keys(users[2])
    driver.find_element(By.ID, "password").send_keys(users[3])
    driver.find_element(By.ID, "password-confirmation").send_keys(users[3])
    time.sleep(3)
    driver.find_element(By.XPATH, '//span[text()="Create an Account"]').click()
    webdriver.support.ui.WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="My Account"]')))

    # Verify that the user is logged in
    assert driver.find_element(By.XPATH, '//span[text()="My Account"]').is_displayed()
    time.sleep(5)


test_eh_sign_up_error_notification = [
    ["Aviram", "Cohen", "mail01yahoo.com", "Aaaaaaa123"],
    [" ", "Rubinstein", "mail01@gmail.com", "aaaaaaA123"],
    ["Aviram", " ", "mail01@gmail.com", "aaaaaaA123"],
    ["Aviram", "Cohen", "mail01@yahoo", "Aaaaaaa123"]
]


# 4 Warning notices upon registration: First name missing. Last name missing. "@" or ".com" missing.
@pytest.mark.parametrize("users", test_eh_sign_up_error_notification)
def test_eh_sign_up_error_notification(setup, users):
    driver = setup

    driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div/ul/li[3]/a').click()
    webdriver.support.ui.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstname")))

    first_name = driver.find_element(By.ID, "firstname")
    first_name.send_keys(users[0])

    last_name = driver.find_element(By.ID, "lastname")
    last_name.send_keys(users[1])

    mail = driver.find_element(By.ID, "email_address")
    mail.send_keys(users[2])

    password = driver.find_element(By.ID, "password")
    password.send_keys(users[3])

    confirm_password = driver.find_element(By.ID, "password-confirmation")
    confirm_password.send_keys(users[3])
    time.sleep(3)

    create_button = driver.find_element(By.XPATH, '//span[text()="Create an Account"]')
    create_button.click()

    time.sleep(3)


    if "@" not in users[2]:
        error_message = driver.find_element(By.ID, "email_address-error").text
        assert error_message == "Please enter a valid email address (Ex: johndoe@domain.com)."


    if not users[0].strip():
        error_message = driver.find_element(By.ID, "firstname-error").text
        assert error_message == "This is a required field."

    if not users[1].strip():
        error_message = driver.find_element(By.ID, "lastname-error").text
        assert error_message == "This is a required field."


    if ".com" not in users[2]:
        error_message = driver.find_element(By.ID, "email_address-error").text
        assert error_message == "Please enter a valid email address (Ex: johndoe@domain.com)."

    time.sleep(5)


def test_fn_purchase_hoodie(setup):
    driver = setup

    navigate_to_hoodie = driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div/div/ol/li[4]/div/div/strong/a')
    driver.execute_script("arguments[0].scrollIntoView(true);", navigate_to_hoodie)
    time.sleep(3)
    navigate_to_hoodie.click()
    time.sleep(3)

    scroll_to_hoodie = driver.find_element(By.ID, 'qty')
    driver.execute_script("arguments[0].click();", scroll_to_hoodie)
    time.sleep(3)

    size = driver.find_element(By.XPATH, '//div[@id="option-label-size-143-item-166"]')
    size.click()

    color = driver.find_element(By.ID, "option-label-color-93-item-53")
    color.click()

    qty = driver.find_element(By.ID, "qty")
    qty.clear()
    driver.find_element(By.ID, "qty").send_keys("2")
    time.sleep(3)

    add_to_cart = driver.find_element(By.ID, "product-addtocart-button")
    add_to_cart.click()
    time.sleep(7)

    driver.execute_script("scrollBy(0,-500);")
    time.sleep(7)

    view_cart = driver.find_element(By.XPATH, '//a[@class="action showcart"]')
    view_cart.click()
    time.sleep(3)

    proceed_to_checkout = driver.find_element(By.XPATH, '//button[@class="action primary checkout"]')
    proceed_to_checkout.click()

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.ID, "customer-email")))

    navigate_to_email = driver.find_element(By.ID, 'customer-email')
    driver.execute_script("arguments[0].scrollIntoView(true);", navigate_to_email)
    time.sleep(3)

    email = driver.find_element(By.ID, "customer-email")
    email.send_keys("Aviram303@example.com")
    time.sleep(3)

    first_name = driver.find_element(By.XPATH, '//input[@name="firstname"]')
    first_name.send_keys("Aviram")

    last_name = driver.find_element(By.XPATH, '//input[@name="lastname"]')
    last_name.send_keys("Katz")

    street_address = driver.find_element(By.XPATH, '//input[@name="street[0]"]')
    street_address.send_keys("Haifa")

    city = driver.find_element(By.XPATH, '//input[@name="city"]')
    city.send_keys("Haifa")

    zip_code = driver.find_element(By.XPATH, '//input[@name="postcode"]')
    zip_code.send_keys("345264")

    select = Select(driver.find_element(By.XPATH, '//select[@name="country_id"]'))
    select.select_by_visible_text("Israel")

    phone = driver.find_element(By.XPATH, '//input[@name="telephone"]')
    phone.send_keys("123456789")
    time.sleep(5)

    continue_to_shipping = driver.find_element(By.XPATH, '//button[@class="button action continue primary"]')
    continue_to_shipping.click()
    time.sleep(3)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="action primary checkout"]')))

    place_order_button = driver.find_element(By.XPATH, '//button[@class="action primary checkout"]')
    place_order_button.click()
    time.sleep(3)

    # Purchase confirmation
    assert driver.find_element(By.XPATH, '//span[text()="Thank you for your purchase!"]').is_displayed()

    time.sleep(5)


def test_fn_sort_by_price_asc(setup):
    driver = setup

    navigate_to_sale = driver.find_element(By.XPATH, '//a[@id="ui-id-8"]')
    navigate_to_sale.click()

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Sale"]')))

    hoodies_and_sweatshirts = driver.find_element(By.XPATH, '//a[text()="Hoodies and Sweatshirts"]')
    hoodies_and_sweatshirts.click()
    time.sleep(3)

    # Select the "Price" option from the Sort By drop-down
    sort_by_price = Select(driver.find_element(By.XPATH, '//select[@class="sorter-options"]'))
    sort_by_price.select_by_visible_text("Price")
    time.sleep(5)

    # waiting for the list of products to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product")))

    # get a list of prices on the page
    prices = driver.find_elements(By.CLASS_NAME, "price")

    prices_numeric = []
    for price in prices:
        if price.text.strip():  # check if string is not empty after stripping whitespace
            prices_numeric.append(float(price.text.replace("$", "")))

    # check that the price list is sorted in ascending order
    assert prices_numeric == sorted(prices_numeric)
    time.sleep(5)


def test_fn_sort_by_product_name_asc(setup):
    driver = setup

    navigate_to_sale = driver.find_element(By.XPATH, '//a[@id="ui-id-8"]')
    navigate_to_sale.click()

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Sale"]')))

    hoodies_and_sweatshirts = driver.find_element(By.XPATH, '//a[text()="Hoodies and Sweatshirts"]')
    hoodies_and_sweatshirts.click()
    time.sleep(3)

    # Select the "Price" option from the Sort By drop-down
    sort_by_price = Select(driver.find_element(By.XPATH, '//select[@class="sorter-options"]'))
    sort_by_price.select_by_visible_text("Product Name")
    time.sleep(5)

    # Get the product names after sorting by name
    products = driver.find_elements(By.XPATH, '//a[@class="product-item-link"]')
    product_names = []
    for product in products:
        product_names.append(product.text)

    # Check if the product names are sorted in ascending order
    assert product_names == sorted(product_names), "Products are not sorted by name A-Z"
    time.sleep(5)


def test_fn_add_to_wish_list(setup):
    driver = setup

    sign_in = driver.find_element(By.LINK_TEXT, "Sign In")
    sign_in.click()

    email = driver.find_element(By.ID, "email")
    email.send_keys("abc444@yahoo.com")
    password = driver.find_element(By.ID, "pass")
    password.send_keys("112233bbC0")
    sign_in_button = driver.find_element(By.ID, "send2")
    sign_in_button.click()

    navigate_to_hoodie = driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div/div/ol/li[4]/div/div/strong/a')
    driver.execute_script("arguments[0].scrollIntoView(true);", navigate_to_hoodie)
    time.sleep(3)

    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div/div/ol/li[4]/div/div/strong/a')).perform()
    time.sleep(3)

    add_to_wish_list = driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div/div[2]/div[3]/div/div/ol/li[4]/div/div/div[3]/div/div[2]/a[1]')
    add_to_wish_list.click()
    time.sleep(3)

    # Verify Hero Hoodie has been added to Wish List
    assert driver.find_element(By.XPATH,
    "//*[contains(text(), 'Hero Hoodie has been added to your Wish List. Click')]").is_displayed()
    time.sleep(3)


def test_fn_remove_from_wish_list(setup):
    driver = setup

    # Sign in
    sign_in = driver.find_element(By.LINK_TEXT, "Sign In")
    sign_in.click()
    email = driver.find_element(By.ID, "email")
    email.send_keys("abc444@yahoo.com")
    password = driver.find_element(By.ID, "pass")
    password.send_keys("112233bbC0")
    sign_in_button = driver.find_element(By.ID, "send2")
    sign_in_button.click()
    time.sleep(3)

    menu_click = driver.find_element(By.XPATH,
    '/html/body/div[1]/header/div[1]/div/ul/li[2]/span/button')
    menu_click.click()
    time.sleep(3)

    wish_list_click = driver.find_element(By.XPATH, '//span[text()="1 item"]')
    wish_list_click.click()
    time.sleep(3)

    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[2]/div[1]/form/div[1]/ol/li/div/strong/a')).perform()
    time.sleep(3)

    remove_hoodie_from_wish_list = driver.find_element(By.XPATH, '//a[@title="Remove Item"]')
    remove_hoodie_from_wish_list.click()
    time.sleep(3)

    # Verify Hero Hoodie has been removed from Wish List
    assert driver.find_element(By.XPATH,
    "//*[contains(text(), 'Hero Hoodie has been removed from your Wish List.')]").is_displayed()

    time.sleep(3)


def test_fn_add_to_comparison_list(setup):
    driver = setup

    # navigate to 'Sale' page
    navigate_to_sale = driver.find_element(By.ID, "ui-id-8")
    navigate_to_sale.click()
    time.sleep(3)

    # navigate to Hoodies and Sweatshirts
    driver.find_element(By.XPATH,
    '//a[text()="Hoodies and Sweatshirts"]').click()
    time.sleep(3)

    # add first item
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div[1]/div[3]/ol/li[1]/div/div')).perform()
    driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div[1]/div[3]/ol/li[1]/div/div/div[3]/div/div[2]/a[2]').click()
    time.sleep(3)

    # add second item
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div[1]/div[3]/ol/li[2]/div/div')).perform()
    driver.find_element(By.XPATH,
    '/html/body/div[1]/main/div[3]/div[1]/div[3]/ol/li[2]/div/div/div[3]/div/div[2]/a[2]').click()
    time.sleep(3)

    # navigate to comparison list
    comparison_list = driver.find_element(By.XPATH, '//a[text()="comparison list"]')
    comparison_list.click()
    time.sleep(3)

    # verify that both items are displayed in comparison list
    element1 = driver.find_element(By.XPATH, '(//a[@title="Eos V-Neck Hoodie"])[2]')
    element2 = driver.find_element(By.XPATH, '(//a[@title="Circe Hooded Ice Fleece"])[2]')
    assert element1.is_displayed() and element2.is_displayed()

    time.sleep(3)


def test_edit_cart_qty(setup):
    driver = setup

    sign_in = driver.find_element(By.LINK_TEXT, "Sign In")
    sign_in.click()

    email = driver.find_element(By.ID, "email")
    email.send_keys("abc444@yahoo.com")
    password = driver.find_element(By.ID, "pass")
    password.send_keys("112233bbC0")
    sign_in_button = driver.find_element(By.ID, "send2")
    sign_in_button.click()
    time.sleep(3)

    click_on_cart = driver.find_element(By.XPATH, '/html/body/div[1]/header/div[2]/div[1]/a')
    click_on_cart.click()
    time.sleep(3)

    click_on_view_cart = driver.find_element(By.LINK_TEXT, "View and Edit Cart")
    click_on_view_cart.click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Shopping Cart"]')))
    time.sleep(3)

    clear_qty = driver.find_element(By.XPATH, '//input[@id="cart-87902-qty"]')
    clear_qty.clear()  # clear the quantity
    time.sleep(3)

    enter_qty = driver.find_element(By.XPATH, '//input[@id="cart-87902-qty"]')
    enter_qty.send_keys("3")  # enter new quantity
    time.sleep(3)

    update_shopping_cart = driver.find_element(By.XPATH, '//span[text()="Update Shopping Cart"]')
    update_shopping_cart.click()  # click on update shopping cart
    time.sleep(3)

    assert driver.find_element(By.XPATH, '//input[@id="cart-87902-qty"][@value="3"]')  # verify quantity is 3


def test_search_hoodie(setup):
    driver = setup

    driver.find_element(By.ID, "search").send_keys("hoodie")
    driver.find_element(By.ID, "search").send_keys(Keys.ENTER)
    time.sleep(3)

    assert driver.find_element(By.XPATH, '//div[text()="XS"]')  # verify XS size is displayed

    time.sleep(3)

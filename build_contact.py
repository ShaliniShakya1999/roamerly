import os
import glob
import re

contact_content = """
    <!-- Hero Section -->
    <section class="hero-slider" style="height: 60vh;">
        <div class="swiper hero-swiper" style="height: 100%;">
            <div class="swiper-wrapper">
                <div class="swiper-slide">
                    <img src="https://images.unsplash.com/photo-1528702748617-c64d49f918af?auto=format&fit=crop&w=1920&q=80" class="hero-img" alt="Contact Us" style="height: 100%; object-fit: cover;">
                    <div class="hero-overlay"></div>
                </div>
            </div>
        </div>

        <div class="hero-content text-center" style="top: 50%;">
            <h1 class="gsap-zoom-in">Get In <span class="text-gradient">Touch</span></h1>
            <p class="gsap-fade-up">We are here to help you 24 hours a day / 7 days a week</p>
        </div>
    </section>

    <!-- Contact Form & Info -->
    <section class="py-5" style="margin-top: -80px; position: relative; z-index: 10;">
        <div class="container">
            <div class="row g-5">
                <!-- Form -->
                <div class="col-lg-7 gsap-fade-up">
                    <div class="glass-card p-5 h-100 border-primary">
                        <h3 class="mb-4">Send Us a Message</h3>
                        <form>
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label text-muted">First Name</label>
                                    <input type="text" class="form-control p-3 bg-transparent border-secondary text-white" placeholder="John">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label text-muted">Last Name</label>
                                    <input type="text" class="form-control p-3 bg-transparent border-secondary text-white" placeholder="Doe">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label text-muted">Email Address</label>
                                    <input type="email" class="form-control p-3 bg-transparent border-secondary text-white" placeholder="john@example.com">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label text-muted">Phone Number</label>
                                    <input type="tel" class="form-control p-3 bg-transparent border-secondary text-white" placeholder="+44 123 456 7890">
                                </div>
                                <div class="col-12">
                                    <label class="form-label text-muted">Subject</label>
                                    <input type="text" class="form-control p-3 bg-transparent border-secondary text-white" placeholder="How can we help you?">
                                </div>
                                <div class="col-12">
                                    <label class="form-label text-muted">Message</label>
                                    <textarea class="form-control p-3 bg-transparent border-secondary text-white" rows="5" placeholder="Write your message here..."></textarea>
                                </div>
                                <div class="col-12 mt-4">
                                    <button type="button" class="btn-luxury w-100 py-3">Send Message</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Info Cards -->
                <div class="col-lg-5 gsap-stagger-container">
                    <div class="glass-card p-4 mb-4 d-flex align-items-center gsap-stagger-item">
                        <div class="fs-1 text-primary me-4"><i class="fas fa-phone-volume"></i></div>
                        <div>
                            <h5 class="mb-1">Call Us</h5>
                            <h4 class="text-gradient mb-0 fw-bold">0204 553 5491</h4>
                            <p class="small text-muted mb-0 mt-1">Available 24/7</p>
                        </div>
                    </div>
                    
                    <div class="glass-card p-4 mb-4 d-flex align-items-center gsap-stagger-item">
                        <div class="fs-1 text-info me-4"><i class="fas fa-envelope-open-text"></i></div>
                        <div>
                            <h5 class="mb-1">Email Us</h5>
                            <p class="lead mb-0 text-white">info@roamerly.co.uk</p>
                            <p class="small text-muted mb-0 mt-1">We'll reply within 2 hours</p>
                        </div>
                    </div>
                    
                    <div class="glass-card p-4 d-flex align-items-center gsap-stagger-item">
                        <div class="fs-1 text-warning me-4"><i class="fas fa-map-marker-alt"></i></div>
                        <div>
                            <h5 class="mb-1">Visit Us</h5>
                            <p class="text-muted mb-0">Suite B6:02C Vista Centre<br>Salisbury Road, Hounslow<br>TW4 6JQ United Kingdom</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Map Section -->
    <section class="py-5 bg-darker">
        <div class="container gsap-fade-up">
            <div class="glass-card p-2">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2484.502014167909!2d-0.3846660842308197!3d51.48564267963162!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x487672ccb89fffff%3A0x868b31ea67bf9f43!2sVista%20Centre%2C%2050%20Salisbury%20Rd%2C%20Hounslow%20TW4%206JQ%2C%20UK!5e0!3m2!1sen!2sin!4v1689163259837!5m2!1sen!2sin" width="100%" height="450" style="border:0; border-radius: 12px;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
        </div>
    </section>
"""

# Read index.html to use as a template
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Replace everything between the navbar end and footer start
# In index.html, it's between <!-- Hero Slider & Advanced Search --> and <!-- Comprehensive Footer -->
start_tag = '    <!-- Hero Slider & Advanced Search -->'
end_tag = '    <!-- Comprehensive Footer -->'

start_idx = index_content.find(start_tag)
end_idx = index_content.find(end_tag)

if start_idx != -1 and end_idx != -1:
    contact_page = index_content[:start_idx] + contact_content + "\n" + index_content[end_idx:]
    contact_page = contact_page.replace('<title>Roamerly - Luxury Travel & Adventures</title>', '<title>Contact Us | Roamerly</title>')
    contact_page = contact_page.replace('href="#contact"', 'href="contact.html"')
    
    with open('contact.html', 'w', encoding='utf-8') as f:
        f.write(contact_page)
    print("Created contact.html")
else:
    print("Error finding tags in index.html")

# Update all existing HTML files to point to contact.html instead of #contact
html_files = glob.glob('*.html')
count = 0
for file in html_files:
    if file == 'contact.html':
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace('href="#contact"', 'href="contact.html"')
    
    if new_content != content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated links in {file}")

print(f"Total files updated with new contact link: {count}")

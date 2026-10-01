const nav = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
const forms = document.querySelectorAll('.contact-form');
const revealItems = document.querySelectorAll('.reveal');
const counters = document.querySelectorAll('.stat-counter');
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightbox-image');
const lightboxClose = document.querySelector('.lightbox-close');
const lightboxPrev = document.querySelector('.lightbox-prev');
const lightboxNext = document.querySelector('.lightbox-next');
const yearNode = document.getElementById('year');
const galleryGrid = document.getElementById('gallery-grid');
let galleryItems = [];

const galleryImages = [
  'assets/images/image1.jpeg',
  'assets/images/image2.jpeg',
  'assets/images/image3.jpeg',
  'assets/images/image4.jpeg',
  'assets/images/image11.jpeg',
  'assets/images/image6.jpeg',
  'assets/images/image7.jpeg',
  'assets/images/image8.jpeg',
  'assets/images/image9.jpeg',
  'assets/images/image10.jpeg'
];

const renderGallery = () => {
  if (!galleryGrid || galleryImages.length === 0) return;

  galleryGrid.innerHTML = '';

  galleryImages.forEach((src, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'gallery-item reveal';
    button.dataset.index = String(index);
    button.setAttribute('aria-label', `Open project gallery image ${index + 1}`);

    if (index % 5 === 1) button.classList.add('tall');
    if (index % 7 === 0) button.classList.add('wide');

    const img = document.createElement('img');
    img.src = src;
    img.alt = `Construction project photo ${index + 1}`;
    img.loading = 'lazy';
    button.appendChild(img);
    galleryGrid.appendChild(button);
  });

  galleryItems = galleryGrid.querySelectorAll('.gallery-item');

  galleryItems.forEach((item) => {
    item.addEventListener('click', () => {
      const itemIndex = Number(item.dataset.index ?? 0);
      openLightbox(itemIndex);
    });
  });

  galleryItems.forEach((item) => revealObserver.observe(item));
};

if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}

const toggleHeader = () => {
  if (!nav) return;
  nav.classList.toggle('scrolled', window.scrollY > 30);
};

toggleHeader();
window.addEventListener('scroll', toggleHeader);

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.18 }
);

revealItems.forEach((item) => revealObserver.observe(item));

const animateCounter = (counter) => {
  const target = Number(counter.dataset.target || 0);
  const duration = 1200;
  const start = performance.now();

  const tick = (time) => {
    const progress = Math.min((time - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const currentValue = Math.round(target * eased);
    counter.textContent = `${currentValue}${target >= 100 ? '+' : ''}`;

    if (progress < 1) {
      requestAnimationFrame(tick);
    } else {
      counter.textContent = `${target}+`;
    }
  };

  requestAnimationFrame(tick);
};

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.4 }
);

counters.forEach((counter) => counterObserver.observe(counter));

let lightboxIndex = 0;

const openLightbox = (index) => {
  if (!lightbox || !lightboxImage) return;

  const safeIndex = (index + galleryImages.length) % galleryImages.length;
  lightboxIndex = safeIndex;
  lightboxImage.src = galleryImages[safeIndex];
  lightbox.classList.add('active');
  lightbox.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
};

const closeLightbox = () => {
  if (!lightbox) return;
  lightbox.classList.remove('active');
  lightbox.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
};

const updateLightbox = (direction) => {
  lightboxIndex = (lightboxIndex + direction + galleryImages.length) % galleryImages.length;
  lightboxImage.src = galleryImages[lightboxIndex];
};

renderGallery();

if (lightboxClose) {
  lightboxClose.addEventListener('click', closeLightbox);
}

if (lightboxPrev) {
  lightboxPrev.addEventListener('click', () => updateLightbox(-1));
}

if (lightboxNext) {
  lightboxNext.addEventListener('click', () => updateLightbox(1));
}

if (lightbox) {
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });
}

document.addEventListener('keydown', (event) => {
  if (!lightbox || !lightbox.classList.contains('active')) return;

  if (event.key === 'Escape') closeLightbox();
  if (event.key === 'ArrowRight') updateLightbox(1);
  if (event.key === 'ArrowLeft') updateLightbox(-1);
});

forms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const status = form.querySelector('.form-status');
    const values = Object.fromEntries(formData.entries());

    const requiredFields = ['fullName', 'phone', 'email', 'projectType', 'message'];
    const invalid = requiredFields.some((field) => !String(values[field] || '').trim());

    if (invalid) {
      if (status) {
        status.textContent = 'Please complete all required fields before sending your enquiry.';
      }
      return;
    }

    if (status) {
      status.textContent = 'Thank you. Your enquiry has been prepared and is ready to be sent.';
    }

    form.reset();
  });
});

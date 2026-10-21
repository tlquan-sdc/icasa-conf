(() => {
  document.documentElement.classList.add('js');
  const data = window.ICASA_SITE || { announcements: [], deadlines: [] };
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const finishLoading = () => {
    const started = window.__ICASA_LOAD_START || 0;
    const minimum = reduceMotion ? 0 : 650;
    window.setTimeout(() => document.documentElement.classList.remove('is-loading'), Math.max(0, minimum - (performance.now() - started)));
  };
  if (document.readyState !== 'loading') finishLoading();
  else document.addEventListener('DOMContentLoaded', finishLoading, { once: true });

  const toggle = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  const setMenu = (open) => {
    if (!toggle || !nav) return;
    nav.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  };
  toggle?.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setMenu(false);
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1100) setMenu(false);
  });

  const clock = document.querySelector('[data-live-time]');
  const updateClock = () => {
    if (!clock) return;
    try {
      clock.textContent = new Intl.DateTimeFormat('en-GB', {
        timeZone: data.timeZone || 'Asia/Ho_Chi_Minh',
        hour: '2-digit', minute: '2-digit', hour12: false
      }).format(new Date()) + ' ICT';
    } catch (_) {
      clock.textContent = 'UTC+7';
    }
  };
  updateClock();
  window.setInterval(updateClock, 30000);

  const announcement = document.querySelector('[data-announcement]');
  const count = document.querySelector('[data-announcement-count]');
  const prev = document.querySelector('[data-announcement-prev]');
  const next = document.querySelector('[data-announcement-next]');
  const pause = document.querySelector('[data-announcement-pause]');
  let announcementIndex = 0;
  let announcementPaused = reduceMotion;
  let announcementTimer;
  const renderAnnouncement = () => {
    if (!announcement || !data.announcements?.length) return;
    const item = data.announcements[announcementIndex];
    announcement.innerHTML = `<time>${item.date}</time><h3>${item.title}</h3><a class="text-link" href="${item.href}">${item.linkLabel} <span>→</span></a>`;
    if (count) count.textContent = `${String(announcementIndex + 1).padStart(2, '0')} / ${String(data.announcements.length).padStart(2, '0')}`;
  };
  const stepAnnouncement = (direction) => {
    announcementIndex = (announcementIndex + direction + data.announcements.length) % data.announcements.length;
    renderAnnouncement();
  };
  const scheduleAnnouncements = () => {
    window.clearInterval(announcementTimer);
    if (!announcementPaused && data.announcements?.length > 1) {
      announcementTimer = window.setInterval(() => stepAnnouncement(1), 6500);
    }
  };
  if (announcement) {
    renderAnnouncement();
    scheduleAnnouncements();
    prev?.addEventListener('click', () => { stepAnnouncement(-1); scheduleAnnouncements(); });
    next?.addEventListener('click', () => { stepAnnouncement(1); scheduleAnnouncements(); });
    pause?.addEventListener('click', () => {
      announcementPaused = !announcementPaused;
      pause.textContent = announcementPaused ? 'Play' : 'Pause';
      pause.setAttribute('aria-label', announcementPaused ? 'Play announcements' : 'Pause announcements');
      scheduleAnnouncements();
    });
  }

  document.querySelectorAll('[data-deadlines]').forEach((list) => {
    const limit = Number(list.dataset.limit || data.deadlines.length);
    list.innerHTML = data.deadlines.slice(0, limit).map((item, index) => `
      <article class="deadline-row" data-reveal>
        <span>${String(index + 1).padStart(2, '0')}</span>
        <h3>${item.label}</h3>
        <time${item.iso ? ` datetime="${item.iso}"` : ''}>${item.value}</time>
      </article>`).join('');
  });

  document.querySelectorAll('[data-filter-group]').forEach((group) => {
    const buttons = [...group.querySelectorAll('[data-filter]')];
    const directory = group.parentElement.querySelector('[data-committee-directory]');
    const committeeGroups = directory ? [...directory.querySelectorAll('[data-committee-group]')] : [];
    const count = group.parentElement.querySelector('[data-committee-count]');
    buttons.forEach((button) => button.addEventListener('click', () => {
      const value = button.dataset.filter;
      buttons.forEach((candidate) => {
        const active = candidate === button;
        candidate.classList.toggle('active', active);
        candidate.setAttribute('aria-pressed', String(active));
      });
      committeeGroups.forEach((committeeGroup) => {
        committeeGroup.hidden = value !== 'all' && committeeGroup.dataset.committeeGroup !== value;
      });
      const visibleMembers = committeeGroups
        .filter((committeeGroup) => !committeeGroup.hidden)
        .reduce((total, committeeGroup) => total + committeeGroup.querySelectorAll('[data-committee-category]').length, 0);
      if (count) count.textContent = `${visibleMembers} ${visibleMembers === 1 ? 'committee member' : 'committee members'}`;
    }));
  });

  document.querySelectorAll('[data-attendee-tabs]').forEach((tabList) => {
    const tabs = [...tabList.querySelectorAll('[role="tab"]')];
    const panels = tabs.map((tab) => document.getElementById(tab.getAttribute('aria-controls'))).filter(Boolean);
    const activateTab = (tab, updateHash = true) => {
      tabs.forEach((candidate) => {
        const active = candidate === tab;
        candidate.classList.toggle('active', active);
        candidate.setAttribute('aria-selected', String(active));
        candidate.tabIndex = active ? 0 : -1;
      });
      panels.forEach((panel) => { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
      if (updateHash) history.replaceState(null, '', `#${tab.dataset.attendeeTab}`);
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activateTab(tab));
      tab.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        const nextIndex = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
        tabs[nextIndex].focus();
        activateTab(tabs[nextIndex]);
      });
    });
    const requested = location.hash.slice(1);
    activateTab(tabs.find((tab) => tab.dataset.attendeeTab === requested) || tabs[0], false);
  });

  document.querySelectorAll('[data-sponsors-section]').forEach((section) => {
    const sponsors = data.sponsors || [];
    const rail = section.querySelector('[data-sponsors]');
    if (!sponsors.length || !rail) return;
    rail.innerHTML = sponsors.map((sponsor) => `
      <a class="sponsor-card" href="${sponsor.href}" target="_blank" rel="noopener noreferrer">
        <span>${sponsor.tier || 'Sponsor'}</span>
        <img src="${sponsor.logo}" alt="${sponsor.name} logo" loading="lazy">
        <strong>${sponsor.name}</strong>
      </a>`).join('');
    section.hidden = false;
  });

  const revealItems = [...document.querySelectorAll('[data-reveal]')];
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px' });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('revealed'));
  }

  const header = document.querySelector('[data-header]');
  const progress = document.querySelector('.reading-progress span');
  const toTop = document.querySelector('[data-to-top]');
  const handleScroll = () => {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = scrollable > 0 ? window.scrollY / scrollable : 0;
    if (progress) progress.style.width = `${Math.min(100, ratio * 100)}%`;
    header?.classList.toggle('scrolled', window.scrollY > 20);
    toTop?.classList.toggle('visible', window.scrollY > 700);
  };
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
  toTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));
})();

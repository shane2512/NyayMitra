import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import GooeyNav from './GooeyNav';

const NAV_ITEMS = [
  { label: 'Home', href: '/' },
  { label: 'Dashboard', href: '/dashboard' },
  { label: 'Pricing', href: '/pricing' },
  { label: 'Privacy', href: '/legal/privacy' },
  { label: 'Terms', href: '/legal/terms' },
  { label: 'Security', href: '/legal/security' }
];

const GooeyNavBar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  // Determine active index based on current route
  const activeIndex = Math.max(
    0,
    NAV_ITEMS.findIndex(item => location.pathname.startsWith(item.href) && item.href !== '/') ||
    NAV_ITEMS.findIndex(item => location.pathname === item.href)
  );

  const handleNav = (item, index) => {
    if (location.pathname !== item.href) {
      navigate(item.href);
    }
  };

  return (
    <div style={{ position: 'relative', zIndex: 50, background: 'transparent', padding: '1.5rem 0 0.5rem 0' }}>
      <GooeyNav
        items={NAV_ITEMS.map((item, idx) => ({
          ...item,
          href: '#',
          onClick: () => handleNav(item, idx)
        }))}
        initialActiveIndex={activeIndex}
        particleCount={15}
        particleDistances={[90, 10]}
        particleR={100}
        animationTime={600}
        timeVariance={300}
        colors={[1, 2, 3, 1, 2, 3, 1, 4]}
      />
    </div>
  );
};

export default GooeyNavBar;

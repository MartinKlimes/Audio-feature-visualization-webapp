export const useHideElement = (hideBtn) => {
  const hide = () => {
    if (hideBtn.value === false) {
      hideBtn.value = true;
      setTimeout(() => {
        hideBtn.value = false;
      }, 2000);
    }
  };

  return {
    hide,
  };
};

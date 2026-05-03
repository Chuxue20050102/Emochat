<script>
export default {}
</script>

<style lang="scss">
page {
  background:
    $emo-page-glow,
    $emo-bg-base;
  color: $emo-text-main;
  font-family: "Avenir Next", "SF Pro Display", "PingFang SC", "Source Han Sans SC", "Microsoft YaHei", sans-serif;
}

.emo-card {
  background: $emo-bg-card;
  border-radius: $emo-radius-base;
  border: 2rpx solid $emo-border-soft;
  box-shadow: $emo-shadow-soft;
  backdrop-filter: blur(20rpx);
}

.emo-btn-primary {
  height: 92rpx;
  border-radius: $emo-radius-pill;
  border: none;
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
  background: linear-gradient(135deg, #5c836f 0%, #3f6d59 100%);
  box-shadow: $emo-shadow-button;
}

.emo-btn-primary::after {
  border: none;
}

.emo-btn-ghost {
  height: 88rpx;
  border-radius: $emo-radius-pill;
  border: 2rpx solid $emo-border-line;
  color: $emo-sage-text;
  font-size: 28rpx;
  background: rgba(255, 255, 255, 0.58);
}

.emo-fade-up {
  animation: emoFadeUp 0.48s cubic-bezier(0.19, 1, 0.22, 1) both;
}

@keyframes emoFadeUp {
  from {
    opacity: 0;
    transform: translateY(18rpx) scale(0.99);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

::-webkit-scrollbar {
  display: none;
  width: 0 !important;
  height: 0 !important;
}
</style>

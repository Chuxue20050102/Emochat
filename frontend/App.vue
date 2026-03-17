<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style lang="scss">
	/* 每个页面公共 CSS */
	page {
		/* 直接采用燕麦奶油白作为全局背景色 */
		background-color: $emo-bg-base;
		/* 统一个文字颜色，去纯黑 */
		color: $emo-text-main;
		/* 字体选用无衬线偏圆润体系 (由系统自动降级) */
		font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
	}

	/* 常用 Flex 布局工具类，方便组员写页面直接使用 */
	.emo-flex-row {
		display: flex;
		flex-direction: row;
		align-items: center;
	}

	.emo-flex-col {
		display: flex;
		flex-direction: column;
	}

	.emo-flex-center {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	/* 全局纸张卡片通用类 */
	.emo-card {
		background-color: $emo-bg-card;
		border-radius: $emo-radius-base;
		box-shadow: $emo-shadow-bubble;
		padding: 30rpx;
		margin-bottom: 24rpx;
	}

	/* 全局药丸主按钮 */
	.emo-pill-btn {
		height: 96rpx;
		border-radius: 48rpx;
		background: linear-gradient(135deg, #FF9B8C, #FFB0A4);
		color: #FFF;
		font-size: 32rpx;
		font-weight: 600;
		letter-spacing: 2rpx;
		display: flex;
		justify-content: center;
		align-items: center;
		box-shadow: 0 12rpx 30rpx rgba(255, 176, 164, 0.35);
		border: none;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}
	.emo-pill-btn::after { border: none; }
	.emo-pill-btn:active {
		transform: scale(0.97);
		box-shadow: 0 6rpx 16rpx rgba(255, 176, 164, 0.3);
	}

	/* 全局统一入场动画 */
	.emo-fade-in {
		animation: emoFadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
	}
	@keyframes emoFadeIn {
		from { opacity: 0; transform: translateY(16rpx); }
		to { opacity: 1; transform: translateY(0); }
	}

	/* 隐藏滚动条 */
	::-webkit-scrollbar {
		display: none;
		width: 0 !important;
		height: 0 !important;
		-webkit-appearance: none;
		background: transparent;
	}
</style>

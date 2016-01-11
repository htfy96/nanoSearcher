function bindAnimation(){
	$(".tag_item").each(function(i, target){
		$(target).mouseenter(function(e){
			//stop current animation.
			$(target).stop();
			$(target).find(".taglist").stop(false, true);
			$(target).parent().addClass("curr");
			$(".tag_item").not($(target)).addClass("not_curr");
			$(target).find(".taglist").animate({
				width: "100%",
				height:"72px"
			}, "normal");
			$(target).animate({
				width: "100%",
				height: "100%",
				top: "0",
				left: "0"
			}, "normal");
		});
		$(target).mouseleave(function(e){
			//stop current animation.
			$(target).stop();
			$(target).find(".taglist").stop(false, true);
			$(target).parent().removeClass("curr");
			$(".tag_item").not(target).removeClass("not_curr");
			$(target).find(".taglist").animate({
				width: "60%",
				height:"24px"
			}, "normal");
			$(target).animate({
				width: "200px",
				height: "200px",
				top: "50px",
				left: "50px"
			}, "normal");
		});
	})
}

$(bindAnimation);

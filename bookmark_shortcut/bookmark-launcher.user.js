// ===UserScript===
// @name          Bookmark Launcher
// @description   Launches bookmarks with keyboard shortcuts
// ===/UserScript===

var bookmarkLauncherSetup = (function() {
    var bookmarks = {}, url;

    bookmarks['C'] = 'javascript:(function(){var hash = window.prompt("Hash:"); window.location=`https://github.com/odoo/odoo/commit/${hash}`}());';
    bookmarks['T'] = 'javascript:(function(){var hash = window.prompt("Hash:"); window.location=`https://www.odoo.com/web#cids=1&menu_id=4720&action=333&active_id=49&model=project.task&view_type=form&id=${hash}`}());';

    window.addEventListener('keyup', function() {
        if(event.ctrlKey && event.altKey && !event.shiftKey)
            if(url = bookmarks[String.fromCharCode(event.keyCode)])
                window.open(url);
    });
}());

:::javascript
targetTask = 'Todo';
defaultTaskString = '@flagged(true) @context(Admin & Routines)';

dueDateStrings = {
	today: '@defer(now) @due(5pm)',
	tonight: '@defer(6pm) @due(8pm)',
	weekend: '@defer(next saturday @ 10am) @due(next sunday @ 5pm)'
};

function generateOmnifocusUrl(params = {}){
	let {contentLines = [], target = targetTask, dueTime = dueDateStrings.today} = params;

	contentLines.forEach((line, index, theArray) =>
		theArray[index] = `- ${line} ${dueTime} ${defaultTaskString}`
	);
	content = encodeURIComponent(contentLines.join('\n'));
	return `omnifocus:///paste?target=/task/${target}&content=${content}`;
}

params = {
    contentLines: draft.content.split('\n'),
    dueTime: dueDateStrings[draft.getTag('taskWhen')],
}

draft.defineTag("OFTasks", generateOmnifocusUrl(params));





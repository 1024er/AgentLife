
const ConversationHistory = ({
    conversationHistory
}) => {
    // const conversationHistory2 = [{"林敏": "你好"}, {"徐磊": "我不好"}];
    // console.log(conversationHistory2);

    return (
        <>
            <div className="fixed bottom-8 left-4 w-1/3 h-1/3 bg-gray-600 bg-opacity-30 text-sky-50 align-baseline p-4 font-thin text-xs overflow-auto rounded-md backdrop-blur-sm" style={{ userSelect: 'none' }}>
            {conversationHistory.map((conversation, index) => {
                const key = Object.keys(conversation)[0];
                const value = conversation[key];
                return (
                <div key={index}>
                    <strong className="text-yellow-400">{key}</strong> {value}
                </div>
                );
            })}
            </div>
        </>
    )
}

export default ConversationHistory
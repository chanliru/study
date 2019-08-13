def MLP_prediction():
    years = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
    prediction_list = []
    for year in years:
        # 分割数据集与测试集
        train_start_date = str(year) + '-01-01'
        train_end_date = str(year) + '-10-31'
        test_start_date = str(year) + '-11-01'
        test_end_date = str(year) + '-12-31'
        train = df.ix[train_start_date: train_end_date]
        test = df.ix[test_start_date:test_end_date]

        # 计算情感分数
        sentiment_score_list = []
        for date, row in train.T.iteritems():
            sentiment_score = np.asarray(
                [df.loc[date, 'compound'], df.loc[date, 'neg'], df.loc[date, 'neu'], df.loc[date, 'pos']])
            sentiment_score_list.append(sentiment_score)
        numpy_df_train = np.asarray(sentiment_score_list)

        sentiment_score_list = []
        for date, row in test.T.iteritems():
            sentiment_score = np.asarray(
                [df.loc[date, 'compound'], df.loc[date, 'neg'], df.loc[date, 'neu'], df.loc[date, 'pos']])
            sentiment_score_list.append(sentiment_score)
        numpy_df_test = np.asarray(sentiment_score_list)

        # 创建MLP模型
        mlpc = MLPClassifier(hidden_layer_sizes=(100, 200, 100), activation='relu',
                             solver='lbfgs', alpha=0.005, learning_rate_init=0.001, shuffle=False)  # span = 20 # best 1
        mlpc.fit(numpy_df_train, train['prices'])
        prediction = mlpc.predict(numpy_df_test)

        prediction_list.append(prediction)
        idx = pd.date_range(test_start_date, test_end_date)
        predictions_df_list = pd.DataFrame(data=prediction[0:], index=idx, columns=['prices'])

        difference_test_predicted_prices = offset_value(test_start_date, test, predictions_df_list)
        predictions_df_list['prices'] = predictions_df_list['prices'] + difference_test_predicted_prices
        predictions_df_list

        # 平滑
        predictions_df_list['ewma'] = predictions_df_list["prices"].ewm(span=20, freq='D').mean()
        predictions_df_list['actual_value'] = test['prices']
        predictions_df_list['actual_value_ewma'] = predictions_df_list["actual_value"].ewm(span=20, freq='D').mean()

        predictions_df_list.columns = ['predicted_price', 'average_predicted_price', 'actual_price',
                                       'average_actual_price']
        predictions_df_list.plot()
        predictions_df_list_average = predictions_df_list[['average_predicted_price', 'average_actual_price']]
        predictions_df_list_average.plot()

        plt.show()
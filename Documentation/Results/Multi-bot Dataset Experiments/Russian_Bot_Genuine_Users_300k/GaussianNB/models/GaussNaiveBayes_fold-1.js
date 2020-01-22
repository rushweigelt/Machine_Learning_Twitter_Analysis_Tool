var GaussianNB = function(priors, sigmas, thetas) {

    this.priors = priors;
    this.sigmas = sigmas;
    this.thetas = thetas;

    this.predict = function(features) {
        var likelihoods = new Array(this.sigmas.length);
    
        for (var i = 0, il = this.sigmas.length; i < il; i++) {
            var sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.log(2. * Math.PI * this.sigmas[i][j]);
            }
            var nij = -0.5 * sum;
            sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.pow(features[j] - this.thetas[i][j], 2.) / this.sigmas[i][j];
            }
            nij -= 0.5 * sum;
            likelihoods[i] = Math.log(this.priors[i]) + nij;
        }
    
        var classIdx = 0;
        for (var i = 0, l = likelihoods.length; i < l; i++) {
            classIdx = likelihoods[i] > likelihoods[classIdx] ? i : classIdx;
        }
        return classIdx;
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 8) {

        // Features:
        var features = process.argv.slice(2);

        // Parameters:
        var priors = [0.5221474716164454, 0.4778525283835547];
        var sigmas = [[1.6419691367960159, 0.2808606018256107, 1.0000000000158766e-09, 4.0597920511389e-05, 1.9129582490230406, 0.09977671821569699, 1.5935384026936377, 0.7395069611690238], [0.2698366108211094, 1.6755507542492711, 2.0922052335633343, 2.0926433561843307, 0.00022266409313062473, 1.747422928794704, 0.3490750173979918, 1.1811113770110238]];
        var thetas = [[-0.11200443012129391, -0.21957675353442818, -0.014647583422504714, -0.0018853744997454338, 0.030958740753741082, -0.32142580195970094, 0.032180421450230784, -0.2127780430793558], [0.12238677525770217, 0.23993060593729099, 0.016005353524335464, 0.0020601408795063976, -0.033828487344365124, 0.3512206378273069, -0.0351634127636517, 0.2325016832825307]];

        // Estimator:
        var clf = new GaussianNB(priors, sigmas, thetas);
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}